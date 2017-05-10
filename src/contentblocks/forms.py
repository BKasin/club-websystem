from django import forms

from .models import Block

class BlockForm(forms.ModelForm):
  class Meta:
    model = Block
    fields = ['description', 'datatype', 'published', 'blob']
    widgets = {
      'description':forms.TextInput(attrs={'size': '100'}),
    }
