from django.db import models
from django.utils import timezone
from clubmembers.models import Club, Member

# Create your models here.

class Content(models.Model):
  MARKDOWN = 'md'
  HTML = 'htm'
  TEXT = 'txt'

  id                    = models.AutoField(primary_key=True)
  club                  = models.ForeignKey(Club)
  uniquetitle           = models.CharField(max_length=20, unique=True)
  description           = models.CharField(max_length=100, null=True)
  blob                  = models.TextField()
  published             = models.BooleanField()
  datatype              = models.CharField(max_length=3, choices=((MARKDOWN, 'CommonMark'), (HTML, 'HTML'), (TEXT, 'Raw Text')))
  created_date          = models.DateTimeField(null=True, default=timezone.now)
  created_by_user       = models.ForeignKey(Member, null=True, related_name="content_created")
  edited_date           = models.DateTimeField(null=True, default=timezone.now)
  edited_by_user        = models.ForeignKey(Member, null=True, related_name="content_edited")

  def __unicode__(self): #Python 3.3 is __str__
    return "%s (%s)"%(self.uniquetitle, self.description)
