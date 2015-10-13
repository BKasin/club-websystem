from django.db import models
from django.contrib.sites.models import Site

class Club(models.Model):
  id                    = models.AutoField(
                            primary_key=True)
  site                  = models.OneToOneField(Site)

  name_short            = models.CharField('Name (short version)',
                            max_length=20)
  name_long             = models.CharField('Name (long version)',
                            max_length=120)
  logo_small            = models.CharField('Logo of the club',
                            help_text='Relative path to the small logo, to used on the users profile. Should not begin with a slash. Ex: img/clublogo-club1-sm.png',
                            max_length=100,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null

  def __unicode__(self): #Python 3.3 is __str__
    return self.name_short
