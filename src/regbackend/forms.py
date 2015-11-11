# Derived from the 'default' backend in django-registration-redux

from django import forms
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field, Div, Submit
from crispy_forms.bootstrap import FormActions

from clubmembers.models import Member

class CustomRegistrationForm(UserCreationForm):
  """
  Custom registration form
  """
  class Meta:
      model = Member
      fields = ('username', 'name_first', 'name_last', 'coyote_id', 'email')

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      'username', 'password1', 'password2', 'name_first', 'name_last', 'coyote_id', 'email',
      FormActions(
        Submit('save', 'Submit Request'),
      )
    )
    super(CustomRegistrationForm, self).__init__(*args, **kwargs)

  """
  Force all usernames to be lowercase
  """
  def clean_username(self):
    return self.cleaned_data['username'].lower()
