from django.db import models
from django.contrib.sites.models import Site

from clubdata.models import Club





class RecurringEvent(models.Model):
  DAILY = 100
  WEEKLY = 200
  MONTHLY = 300
  ruletypes = (
    (DAILY, 'Every day'),
    (WEEKLY, 'Specified days of the week'),
    (MONTHLY, 'Specified days of the month'),
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
                            help_text='Repeat every X days/weeks/months.',
                            default=1)
  criteria              = models.CharField('Criteria',
                            max_length=200)

  class Meta:
    verbose_name = 'Recurring Event'
    verbose_name_plural = 'Recurring Events'

  def __unicode__(self): #Python 3.3 is __str__
    return str(self.id)






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
    return self.title
