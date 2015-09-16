from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Member

class MemberForm(forms.ModelForm):
  class Meta:
    model = Member
    fields = ['name_first', 'name_last', 'email', 'phone', 'texting_ok', 'shirt_size', 'acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr']

  def __init__(self, *args, **kwargs):
    h = FormHelper()
    h.form_method = 'post'
    h.add_input(Submit('submit', 'Submit'))
    self.helper = h
    super(MemberForm, self).__init__(*args, **kwargs)
