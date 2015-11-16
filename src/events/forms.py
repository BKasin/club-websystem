from django import forms

from .models import Event

# Form used for editing an event
class EventEditForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'start', 'duration', 'all_day']
