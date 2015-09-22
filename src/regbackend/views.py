from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from registration.users import UserModel

from clubmembers.models import Member

class RegistrationView(BaseRegistrationView):
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

    return new_user

  def registration_allowed(self, request):
    return getattr(settings, 'REGISTRATION_OPEN', True)
