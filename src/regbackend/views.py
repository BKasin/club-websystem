# Derived from the 'default' backend in django-registration-redux

from django.conf import settings
from django.contrib.sites.requests import RequestSite
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction
from transactionalemail import mailer

from registration import signals
from registration.models import RegistrationProfile
from registration.views import ActivationView as BaseActivationView
from registration.views import RegistrationView as BaseRegistrationView

from clubmembers.models import Member

class RegistrationView(BaseRegistrationView):
  send_email = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
  success_url = 'registration_complete'

  @transaction.atomic   # A database transaction is used for this entire function
  def register(self, request, form):
    # Create a new Member instance
    if hasattr(form, 'save'):
      # FYI: This skips our custom MemberManager
      new_user_instance = form.save()
    else:
      # This will pass the data to the create_user function in our custom MemberManager
      new_user_instance = Member.objects.create_user(**form.cleaned_data)

    # Create a RegistrationProfile instance for that user with a one-time activation key
    registration_profile = RegistrationProfile.objects.create_profile(new_user_instance)

    # Send the mail ourselves, so we have control over the templates used
    if self.send_email:
      mailer.send_template_email(request,
        template_prefix='registration/activation_email',
        to=[new_user_instance.email],
        extra_context={
          'user': new_user_instance,
          'activation_key': registration_profile.activation_key,
          'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        }
      )

    # Send the signal that a user has been registered
    signals.user_registered.send(sender=self.__class__,
                   user=new_user_instance,
                   request=request)
    return new_user_instance

  def registration_allowed(self, request):
    return getattr(settings, 'REGISTRATION_OPEN', True)


class ActivationView(BaseActivationView):
  @transaction.atomic   # A database transaction is used for this entire function
  def activate(self, request, activation_key):
    # Attempt to activate the user
    activated_user = RegistrationProfile.objects.activate_user(activation_key)

    if activated_user:
      # Automatically log the user in
      signals.login_user(self, activated_user, request)

      # Send the signal that user has been activated
      signals.user_activated.send(sender=self.__class__,
                    user=activated_user,
                    request=request)

    return activated_user

  def get_success_url(self, request, user):
    return ('registration_activation_complete', (), {})
