from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field, Div, Submit
from crispy_forms.bootstrap import FormActions

class RegistrationFormWithoutEmail(UserCreationForm):
  """
  Custom registration form
  """
  name_first = forms.CharField(max_length=30)
  name_last = forms.CharField(max_length=30)
  email = forms.EmailField(label="E-mail", required=False)

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      'name_first', 'name_last', 'email', 'username', 'password1', 'password2',
      FormActions(
        Submit('save', 'Submit Request'),
      )
    )
    super(RegistrationFormWithoutEmail, self).__init__(*args, **kwargs)
