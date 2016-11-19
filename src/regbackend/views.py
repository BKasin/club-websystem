# Derived from the 'default' backend in django-registration-redux

from django.conf import settings
from django.contrib.sites.requests import RequestSite
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponse
from utils.templateemail import send_template_email

from registration import signals
from registration.models import RegistrationProfile
from registration.views import ActivationView as BaseActivationView
from registration.views import RegistrationView as BaseRegistrationView

from clubmembers.models import Member


def check_username_available(request):
  if Member.objects.filter(username__iexact=request.GET['username'].lower()).exists():
    return HttpResponse('1')
  else:
    return HttpResponse('0')

class RegistrationView(BaseRegistrationView):
  send_email = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
  success_url = 'registration_complete'

  @transaction.atomic   # A database transaction is used for this entire function
  def register(self, form):
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
    # We also use a different template name (instead of activation_email.html), so
    #   send_template_email won't inadvertently pull in the original template
    if self.send_email:
      send_template_email(self.request,
        template_prefix='registration/registration_complete_email',
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
                   request=self.request)
    return new_user_instance

  def registration_allowed(self):
    return getattr(settings, 'REGISTRATION_OPEN', True)


class ActivationView(BaseActivationView):
  @transaction.atomic   # A database transaction is used for this entire function
  def activate(self, *args, **kwargs):
    # Attempt to activate the user
    activation_key = kwargs.get('activation_key', '')
    activated_user = RegistrationProfile.objects.activate_user(activation_key)

    if activated_user:
      # Automatically log the user in
      signals.login_user(self, activated_user, self.request)

      # Send the signal that user has been activated
      signals.user_activated.send(sender=self.__class__,
                    user=activated_user,
                    request=self.request)

    return activated_user

  def get_success_url(self, user):
    return ('registration_activation_complete', (), {})
