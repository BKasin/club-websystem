from datetime import date, timedelta

from django.db import models
from django.contrib.sites.models import Site
from django.core.validators import MinValueValidator

from clubdata.models import Club





def range_date_inclusive(start_date, end_date):
  for n in range((end_date - start_date).days+1):
    yield start_date + timedelta(n)

def num_days_in_month(d):
  dmonth = d.month
  if dmonth == 12:
    return 31
  else:
    return (d.replace(month=dmonth+1, day=1) - timedelta(days=1)).day

def last_day_in_month(d):
  dmonth = d.month
  if dmonth == 12:
    return d.replace(day=31)
  else:
    return d.replace(month=dmonth+1, day=1) - timedelta(days=1)

def decode_weekly_criteria(criteria):
  c = criteria.split(",")
  dow_possible = ('mo','tu','we','th','fr','sa','su')
  dow = [False,False,False,False,False,False,False]
  for x in c: dow[dow_possible.index(x)] = True
  return dow

def decode_monthly_criteria(criteria):
  c = criteria.split(",")
  specificdays = []
  daystocalculate = []
  dow_possible = ('mo','tu','we','th','fr','sa','su')
  for x in c:
    if x.isdigit():
      # Specific numbered day (same every month)
      specificdays.append(int(x))
    else:
      # A code to represent a day. We'll convert from strings to integers for later.
      if x == 'last':
        # Last day of the month (must be calculated later)
        daystocalculate.append( (99, -1) )
      else:
        y,z = x.split("-")
        if y == 'last':
          # Last DOW of the month (must be calculated later)
          daystocalculate.append( (99, dow_possible.index(z)) )
        else:
          # Specified DOW of the month (must be calculated later)
          daystocalculate.append( (int(y), dow_possible.index(z)) )
  return specificdays,daystocalculate





class RecurringEvent(models.Model):
  DAILY = 100
  WEEKLY = 200
  MONTHLY = 300
  ruletypes = (
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
  )

  id                    = models.AutoField(
                            primary_key=True)

  # Range
  starts_on             = models.DateField('Starts on')
  ends_on               = models.DateField('Ends on')

  # Rule
  rule_type             = models.IntegerField('Recurring rule',
                            choices=ruletypes,
                            default=WEEKLY)
  repeat_each           = models.IntegerField('Repeat each',
                            default=1,
                            validators=[MinValueValidator(1)])
  criteria              = models.CharField('Criteria',
                            max_length=200,
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional

  class Meta:
    verbose_name = 'Recurring Event'
    verbose_name_plural = 'Recurring Events'

  def __unicode__(self): #Python 3.3 is __str__
    rt = self.rule_type
    for t in self.ruletypes:
      if t[0] == rt:
        rt = t[1]
        break
    return "%s Event, %s to %s, \"%s\"" % (rt, self.starts_on, self.ends_on, self.criteria)

  def dates_per_rule_iter(self):
    if self.rule_type == self.WEEKLY:
      # criteria = Must be a comma-separated list of lowercase 2-letter abbreviations for the days
      #   of the week. Ex: mo,we,fr,su
      # repeat_each = If this is 2, then every other week (Mon-Sun) will be skipped. If it is 3,
      #   then two weeks (Mon-Sun) will be skipped between each filled week. etc...

      # Deconstruct the criteria
      criteria = decode_weekly_criteria(self.criteria)

      # Generate a list of dates that match
      if self.repeat_each == 1:
        # If repeat_each is 1, then our calculation is much simpler
        for x in range_date_inclusive(self.starts_on, self.ends_on):
          if criteria[x.weekday()]: yield x
      else:
        # Special handling because we're not doing every week
        r = 2 # Set this to 2 so the first iteration will set it to 1
        dow_begin = self.starts_on.weekday()
        for x in range_date_inclusive(self.starts_on, self.ends_on):
          wd = x.weekday()
          if wd == dow_begin:
            # It's the beginning of a new week (rather than assuming the user considers Monday to be
            #   the first day of the week, we use the DOW of the start of the range for this purpose.
            if r == 1:
              # Reset the counter
              r = self.repeat_each
            else:
              # Decrease the counter
              r -= 1
          if r == 1:
            # If counter is 1, then this week should be included
            if criteria[wd]: yield x

    elif self.rule_type == self.MONTHLY:
      # criteria = Must be a comma-separated list of the following types of codes:
      #   * 1,2,3,4, etc                specific days of the month
      #   * 1-mo, 3-fr, last-we, etc    first Monday, third Friday, last Wednesday, etc.
      #   * last                        last day of the month
      # repeat_each = If this is 2, then every other month will be skipped. If it is 3, then two
      #   months will be skipped between each filled month. etc...

      # Deconstruct the criteria
      specificdays,daystocalculate = decode_monthly_criteria(self.criteria)

      # Generate a list of dates that match
      calcdays = None
      oneday = timedelta(days=1)
      r = 2 # Set this to 2 so the first iteration will set it to 1
      for x in range_date_inclusive(self.starts_on, self.ends_on):
        xday = x.day
        if (xday == 1) or (calcdays is None):
          # It's the first day of the month (or first iteration of this loop)
          if r == 1:
            # Reset the counter
            r = self.repeat_each
          else:
            # Decrease the counter
            r -= 1
          if r == 1:  # Putting this within the above 'else' will malfunction if repeat_each is 1
            # Since this month is included, we must turn those vague days into specific numbered days
            #   for this current month (each month is different, so they couldn't have been calculated earlier.
            calcdays = []
            for y in daystocalculate:
              if y[0] == 99:
                if y[1] == -1:
                  # Calculate the last day of the month
                  calcdays.append(num_days_in_month(x))
                else:
                  # Calculate the last DOW of the month
                  end_date = last_day_in_month(x)
                  for z in range(end_date.day):
                    d = end_date - timedelta(z)
                    if d.weekday() == y[1]:
                      calcdays.append(d.day)
                      break
              else:
                # Calculate the specified DOW of the month
                start_date = date(x.year, x.month, 1)
                found_count = 0
                for z in range(num_days_in_month(start_date)):
                  d = start_date + timedelta(z)
                  if d.weekday() == y[1]:
                    found_count += 1
                    if found_count == y[0]:
                      calcdays.append(z+1)
                      break
            print(calcdays)
        # Check if this month is included (not a skipped month per the repeat_each rule)
        if r == 1:
          if (xday in specificdays) or (xday in calcdays):
            # Assuming the daystocalculate have been calculated (above), simply check if the day is
            #   in one of the two lists
            yield x

    elif self.rule_type == self.DAILY:
      # criteria = Not used
      # repeat_each = If this is 2, then every other day will be skipped. If it is 3, only every
      #   third day will be chosen. etc...

      # Generate a list of dates that match
      if self.repeat_each == 1:
        # If repeat_each is 1, then our calculation is much simpler
        for x in range_date_inclusive(self.starts_on, self.ends_on):
          yield x
      else:
        # Use the repeat value.
        r = self.repeat_each # Include the first day of the range, and then start counting from there
        for x in range_date_inclusive(self.starts_on, self.ends_on):
          if r == self.repeat_each:
            yield x
            r = 1
          else:
            r += 1





class CustomEventManager(models.Manager):
  # Custom manager to show only the items that either
  #   (a) belong to the current Club, or
  #   (b) belong to no Club
  use_in_migrations = True

  current_club_id = None

  def _get_current_club_id(self):
    if not self.current_club_id:
      current_site = Site.objects.get_current()
      self.current_club_id = current_site.club.id
    return self.current_club_id

  def get_queryset(self):
    return super(CustomEventManager, self).get_queryset().filter(
      models.Q(club=self._get_current_club_id()) | models.Q(club=None))

class Event(models.Model):
  id                    = models.AutoField(
                            primary_key=True)
  club                  = models.ForeignKey(Club, verbose_name='Specific to club',
                            help_text='Only the specified club will show the event on their calendar. If none, event will show on calendars of all clubs.',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            on_delete=models.SET_NULL)  # Deleting a club will leave all associated events behind as global events
  title                 = models.CharField('Title',
                            blank=True, # Field is optional
                            max_length=200)
  start                 = models.DateTimeField('Start date/time',
                            help_text='Specify as <i>yyyy-mm-dd hh:mm</i>')
  duration              = models.DurationField('Duration',
                            help_text='Specify as <i>hh:mm:ss</i>')
  all_day               = models.BooleanField('All day event?',
                            default=False)
  recurring             = models.ForeignKey(RecurringEvent, verbose_name='Belongs to recurring group',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            on_delete=models.SET_NULL)  # Deleting an EventGroup will leave all linked events as isolated events

  objects = CustomEventManager()

  class Meta:
    verbose_name = 'Event'
    verbose_name_plural = 'Events'

  def __unicode__(self): #Python 3.3 is __str__
    return "%s %s" % (self.start, self.title)
