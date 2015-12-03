import re
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import six

from .models import Event, RecurringEvent

re_weekly = re.compile(r'^((mo|tu|we|th|fr|sa|su),)+$')
re_monthly = re.compile(r'^([1-3][0-9],|[1-9],|last,|(([1-5]|last)-(mo|tu|we|th|fr|sa|su)),)+$')


def duration_string(duration):
  """
  This is originally taken from django.utils.duration, but modified to not show seconds by default,
  and to show the "day" or "days" text
  """
  days = duration.days
  seconds = duration.seconds
  microseconds = duration.microseconds

  minutes = seconds // 60
  seconds = seconds % 60

  hours = minutes // 60
  minutes = minutes % 60

  if days:
    if days == 1:
      string = '{} day'.format(days)
    else:
      string = '{} days'.format(days)
  else:
    string = None

  if hours or minutes or seconds or microseconds:
    if string is None:
      string = '{:02d}:{:02d}'.format(hours, minutes)
    else:
      string += ', {:02d}:{:02d}'.format(hours, minutes)
    if seconds:
      string += ':{:02d}'.format(seconds)
    if microseconds:
      string += '.{:06d}'.format(microseconds)

  return string

simple_duration_re = re.compile(
  r'^'
  r'(?:(?P<days>\d+) (days?(?:, )?)?)?'
  r'(?:(?P<hours>\d{1,2}):(?P<minutes>\d{2}))?'
  r'$'
)
def parse_duration(value):
  """
  This is originally taken from django.utils.dateparse, but modified to not allow seconds or microseconds
  """
  match = simple_duration_re.match(value)
  if match:
    kw = match.groupdict()
    kw = {k: float(v) for k, v in six.iteritems(kw) if v is not None}
    return datetime.timedelta(**kw)

class SimpleDurationField(forms.DurationField):
  """
  DurationField modified to use 'duration_string', 'parse_duration', and 'simple_duration_re' from
  above instead of the ones Django provide
  """
  def prepare_value(self, value):
    if isinstance(value, datetime.timedelta):
      return duration_string(value)
    return value

  def to_python(self, value):
    if value in self.empty_values:
      return None
    if isinstance(value, datetime.timedelta):
      return value
    value = parse_duration(value)
    if value is None:
      raise ValidationError(self.error_messages['invalid'], code='invalid')
    return value






class EventEditForm(forms.Form):
  """
  Form for creating and editing both regular and recurring events. This is not a ModelForm, as we need
  special handling for most of the fields.
  """

  NORECURRING = 0
  criteria_help_texts = (
    (RecurringEvent.DAILY, 'Criteria is not used for daily events.'),
    (RecurringEvent.WEEKLY, 'Comma-separated list of 2-letter abbreviations. Example: <i>Mo,We,Fr,Su</i>'),
    (RecurringEvent.MONTHLY, 'Comma-separated list of codes. Example:<i>1,7,2-Mo,26,Last-Fr,Last</i>'
      '<ul>'
        '<li>Days of the month: 1, 17, 24, etc.</li>'
        '<li>Specific instance of a day-of-week: 3-Mo, 1-Fr, Last-Sa, etc.</li>'
        '<li>Last day of the month: Last</li>'
      '</ul>'),
  )

  event_type            = forms.TypedChoiceField(label='Event type',
                            coerce=int,
                            empty_value=NORECURRING,
                            required=False)
  start_date            = forms.DateField(label='<span class="hide-if-onetime">Start of range</span><span class="show-if-onetime">Date</span>',
                            required=False,
                            widget=forms.DateInput(attrs={'type':'date'}))
  end_date              = forms.DateField(label='End of range',
                            required=False,
                            widget=forms.DateInput(attrs={'type':'date'}))
  repeat_each           = forms.IntegerField(label='Repeat',
                            required=False)
  criteria              = forms.CharField(label='Criteria',
                            help_text='<span id="criteria_help_text">&nbsp;</span>',
                            required=False)

  title                 = forms.CharField(label='Title',
                            required=False)
  club_global           = forms.BooleanField(label='Club',
                            required=False)
  start_time            = forms.TimeField(label='Time',
                            required=False,
                            widget=forms.TimeInput(attrs={'type':'time'}))
  duration              = SimpleDurationField(label='Duration',
                            help_text='<i>[D days,] hh:mm</i>',
                            required=False)
  all_day               = forms.BooleanField(label='All day?',
                            required=False)

  def __init__(self, event_type_choices=None, *args, **kwargs):
    super(EventEditForm, self).__init__(*args, **kwargs)
    self.fields['event_type'].choices = event_type_choices

  def current_event_type_choices(self):
    return self.fields['event_type'].choices

  def clean(self):
    super(EventEditForm, self).clean()

    # Some fields are always required, but we handle the validation here for consistency

    if not self.cleaned_data.get('title'):
      self.add_error('title', "This field is required.")

    start_date = self.cleaned_data.get('start_date')
    if start_date is None:
      self.add_error('start_date', "This field is required.")

    if self.cleaned_data.get('duration') is None:
      self.add_error('duration', "This field is required.")

    # Other fields require special handling

    if self.cleaned_data.get('all_day'):
      self.cleaned_data['start_time'] = None
    else:
      if self.cleaned_data.get('start_time') is None:
        self.add_error('start_time', "This field is required.")

    event_type = self.cleaned_data.get('event_type')
    if event_type != self.NORECURRING:
      end_date = self.cleaned_data.get('end_date')
      if end_date is None:
        self.add_error('end_date', "This field is required.")
      elif (not start_date is None) and (end_date < start_date):
        self.add_error('end_date', "May not be less than Start Date.")

      repeat_each = self.cleaned_data.get('repeat_each')
      if repeat_each is None:
        self.add_error('repeat_each', "This field is required.")
      elif repeat_each < 1:
        self.add_error('repeat_each', "Must be at least 1.")

      criteria = self.cleaned_data.get('criteria')
      if event_type == RecurringEvent.WEEKLY:
        if criteria:
          criteria = criteria.replace(' ','').lower()
          if bool(re_weekly.search(criteria + ',')):
            self.cleaned_data['criteria'] = criteria
          else:
            self.add_error('criteria', "Criteria is not in the proper format for weekly events.")
        else:
          self.add_error('criteria', "Weekly events must specify a criteria string.")

      elif event_type == RecurringEvent.MONTHLY:
        if criteria:
          criteria = criteria.replace(' ','').lower()
          if bool(re_monthly.search(criteria + ',')):
            self.cleaned_data['criteria'] = criteria
          else:
            self.add_error('criteria', "Criteria is not in the proper format for monthly events.")
        else:
          self.add_error('criteria', "Monthly events must specify a criteria string.")
