from django.db import models

class Club(models.Model):
  id                    = models.AutoField(
                            primary_key=True)

  name_short            = models.CharField('Name (short version)',
                            max_length=20)
  name_long             = models.CharField('Name (long version)',
                            max_length=120)

  def __unicode__(self): #Python 3.3 is __str__
    return self.name_short
