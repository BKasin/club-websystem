from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field, Div, Submit
from crispy_forms.bootstrap import FormActions

from .models import Member

class MemberForm(forms.ModelForm):
  username = forms.CharField(max_length=254)
  password = ReadOnlyPasswordHashField(
    label="Password*",
    help_text="For your security, we store a hash of your password in the database, instead of the password itself. To update your password, visit the <a href='/accounts/password/change/'><b>Change My Password</b></a> page."
  )
  class Meta:
    model = Member
    fields = [
      'username', 'password', 'name_first', 'name_last',
      'email', 'phone', 'texting_ok',
      'photo',
      'acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',
      'shirt_size',
    ]

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      HTML('<div class="row"><div class="col-sm-6">'),
      Fieldset(
        'Identity',
        'username', Field('password', css_class='nofieldborder'), 'name_first', 'name_last',
      ),
      Fieldset(
        'Contact',
        'email', 'phone', 'texting_ok',
      ),
      HTML('</div><div class="col-sm-6">'),
      Fieldset(
        'Photo',
        HTML('<img style="float:right" src="{{ user.member.photo.thumbnail.100x100 }}" />'),
        'photo',
      ),
      Fieldset(
        'Academic',
        'acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',
      ),
      Fieldset(
        'Other',
        'shirt_size',
      ),
      HTML('</div></div>'),
      FormActions(
        Submit('save', 'Save Changes'),
      )
    )
    super(MemberForm, self).__init__(*args, **kwargs)
