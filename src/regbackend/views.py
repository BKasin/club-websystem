from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from registration.users import UserModel

from clubmembers.models import Member

class RegistrationView(BaseRegistrationView):
  """
  A registration backend which implements the simplest possible
  workflow: a user supplies a username, email address and password
  (the bare minimum for a useful account), and is immediately signed
  up and logged in).

  """
  success_url = 'registration_complete'

  def register(self, request, form):
    # Create the new user
    new_user = form.save()

    # Create the new associated member
    new_member = Member(
      user=new_user,
      name_first=form.cleaned_data['name_first'],
      name_last=form.cleaned_data['name_last'],
      email=form.cleaned_data['email'],
    ).save()

    # Log the user in
    new_user = authenticate(
      username=new_user.username,
      password=form.cleaned_data['password1']
    )
    login(request, new_user)

    # Can we remove this?
    signals.user_registered.send(sender=self.__class__,
                   user=new_user,
                   request=request)
    return new_user

  def registration_allowed(self, request):
    """
    Indicate whether account registration is currently permitted,
    based on the value of the setting ``REGISTRATION_OPEN``. This
    is determined as follows:

    * If ``REGISTRATION_OPEN`` is not specified in settings, or is
      set to ``True``, registration is permitted.

    * If ``REGISTRATION_OPEN`` is both specified and set to
      ``False``, registration is not permitted.

    """
    return getattr(settings, 'REGISTRATION_OPEN', True)
