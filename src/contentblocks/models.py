from django.db import models
from django.utils import timezone
from django.core import validators

from clubdata.models import Club
from clubmembers.models import Member

# Create your models here.
class Block(models.Model):
  MARKDOWN = 'md'
  HTML = 'htm'
  TEXT = 'txt'

  id                    = models.AutoField(
                            primary_key=True)
  club                  = models.ForeignKey(Club, verbose_name='Club which owns the content',
                            help_text='Note: deleting a club will also delete any content associated with it. To avoid that, leave this field blank.',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            on_delete=models.CASCADE)  # Deleting a club will delete all delete all associated content
  uniquetitle           = models.CharField('Unique title',
                            help_text='Use only letters, numbers, underscores or hyphens. This is used internally to lookup this piece of content, so use something short and logical, and use a prefix that can be filtered on later (competition_ccdc, project_securitysystem, etc.)',
                            max_length=20,
                            unique=True,
                            validators=[validators.validate_slug])
  description           = models.CharField('Description',
                            help_text='Longer description, if any.',
                            max_length=100,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  datatype              = models.CharField('Type of content',
                            help_text='This tells the website how to process and render the content for the user.',
                            max_length=3,
                            choices=((MARKDOWN, 'CommonMark'), (HTML, 'HTML'), (TEXT, 'Raw Text')))
  blob                  = models.TextField('Content block',
                            help_text='This is the actual block of content. Specify the format above.')
  published             = models.BooleanField('Published?',
                            help_text='If true, this content will be visible to regular users of the site. False will hide the content without needing to delete it.')
  created_date          = models.DateTimeField('Created on',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            default=timezone.now)
  created_by_user       = models.ForeignKey(Member, verbose_name='Created by',
                            help_text='Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            related_name="content_created",
                            on_delete=models.SET_NULL)  # If a member is deleted, do NOT delete content created by that user!
  edited_date           = models.DateTimeField('Last edited on',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            default=timezone.now)
  edited_by_user        = models.ForeignKey(Member, verbose_name='Last edited by',
                            help_text='Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.',
                            null=True,  # Blank is stored as Null
                            blank=True, # Field is optional
                            related_name="content_edited",
                            on_delete=models.SET_NULL)  # If a member is deleted, do NOT delete content edited by that user!

  def __unicode__(self): #Python 3.3 is __str__
    return "%s (%s)"%(self.uniquetitle, self.description)
