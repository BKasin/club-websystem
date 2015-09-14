from django.db import models

# Create your models here.
class Event(models.Model):
  id                    = models.AutoField(primary_key=True)
  title                 = models.CharField('Title', blank=True, max_length=200)
  start                 = models.DateTimeField('Start')
  end                   = models.DateTimeField('End')
  allDay                = models.BooleanField('All day', default=False)

  def get_start(self):
    return self.start

  class Meta:
      verbose_name = 'Event'
      verbose_name_plural = 'Events'

  def __unicode__(self): #Python 3.3 is __str__
      return "%s to %s: %s (all_day=%s)"%(str(self.start), str(self.end), self.title, str(self.allDay))
