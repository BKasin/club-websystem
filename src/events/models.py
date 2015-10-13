from django.db import models
from django.contrib.sites.models import Site

from clubdata.models import Club

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
                            help_text='This will show directly on the calendar.',
                            blank=True, max_length=200)
  start                 = models.DateTimeField('Start date/time')
  end                   = models.DateTimeField('End date/time')
  allDay                = models.BooleanField('All day event?',
                            default=False)

  objects = CustomEventManager()

  def get_start(self):
    return self.start

  class Meta:
      verbose_name = 'Event'
      verbose_name_plural = 'Events'

  def __unicode__(self): #Python 3.3 is __str__
      return self.title
