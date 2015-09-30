import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnDiscPlaceholderImage

# Create your models here.
class Club(models.Model):
  id                    = models.AutoField(
                            primary_key=True)

  name_short            = models.CharField('Name (short version)',
                            max_length=20)
  name_long             = models.CharField('Name (long version)',
                            max_length=120)

  def __unicode__(self): #Python 3.3 is __str__
    return self.name_short


class Member(models.Model):
  # Extends the built-in User model
  user                  = models.OneToOneField(User, verbose_name='Associated user',
                            help_text='This provides a link to Django\'s built-in user model, which handles attributes such as username, password, permissions, staff status, etc.',
                            primary_key=True)

  # Name
  name_first            = models.CharField('First name',
                            max_length=30)
  name_last             = models.CharField('Last name',
                            max_length=30)

  # Contact info
  email                 = models.EmailField('Email address',
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  phone                 = models.CharField('Phone number',
                            max_length=10,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  texting_ok            = models.BooleanField('May the club send SMS messages to this number?',
                            default=True)

  # Photo of user
  photo                = VersatileImageField('Profile photo',
                            help_text='Upload a photo of yourself (no more than 5MB).',
                            null=True,     # Blank is stored as Null
                            blank=True,    # Field is optional
                            upload_to="memberphotos",
                            width_field="photowidth", height_field="photoheight", #ppoi_field="photoppoi",
                            placeholder_image=OnDiscPlaceholderImage(os.path.join(settings.BASE_DIR, 'clubmembers/placeholder.png')))
  photowidth            = models.PositiveIntegerField(
                            null=True,     # Blank is stored as Null
                            blank=True,    # Field is optional
                            editable=False # Don't show on any forms
                          )
  photoheight           = models.PositiveIntegerField(
                            null=True,     # Blank is stored as Null
                            blank=True,    # Field is optional
                            editable=False # Don't show on any forms
                          )

  # PIN number, used for signing in and out for meetings without requiring the user's full password
  pin_hash              = models.CharField('PIN',
                            help_text='This is optional, but will be used for less critical sign-in purposes, such as checking into a project meeting or confirming your lab hours.',
                            max_length=120,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null

  # Other information we may be interested in
  shirt_size            = models.CharField('Preferred shirt size',
                            help_text='Please use an abbreviation here (XS, S, M, L, XL, XXL, etc.).',
                            max_length=5,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  acad_major            = models.CharField('Major',
                            help_text='List your academic major (Business Administration, Computer Science, etc.)',
                            max_length=50,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  acad_minor            = models.CharField('Minor',
                            help_text='List your academic minor, if any (Business Administration, Computer Science, etc.)',
                            max_length=50,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  acad_concentration    = models.CharField('Concentration',
                            help_text='List your academic concentration, if any (Cybersecurity, etc.)',
                            max_length=50,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  acad_grad_qtr         = models.CharField('Graduation quarter',
                            help_text='Specify your graduation quarter (Spring 2015, Fall 2016, etc.)',
                            max_length=20,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null

  def get_short_name(self):
    return self.name_first

  def get_full_name(self):
    return (self.name_first + ' ' + self.name_last).strip()

  def __unicode__(self): #Python 3.3 is __str__
    return "%s %s <%s>"%(self.name_first, self.name_last, self.email)


class Membership(models.Model):
  id                    = models.AutoField(primary_key=True)

  # Which member is a member of which club
  member                = models.ForeignKey(Member, verbose_name='Member',
                            on_delete=models.CASCADE)  # Deleting a member will delete all memberships that reference it
  club                  = models.ForeignKey(Club, verbose_name='is a member of',
                            on_delete=models.CASCADE)  # Deleting a club will delete all memberships that reference it (won't delete the members themselves)

  # Membership dues
  paid_date             = models.DateField('Paid on',
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional
  paid_until_date       = models.DateField('Payment is valid until',
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional
  paid_amount           = models.DecimalField('Paid amount',
                            max_digits=6,
                            decimal_places=2,
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional
  receipt_date          = models.DateField('Receipt sent to member on',
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional

  # Club badges (if applicable)
  badge_issue_date      = models.DateField('Badge issued on',
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional
  badge_type            = models.CharField('Type of badge issued',
                            max_length=20,
                            blank=True) # Field is optional, but blank is stored as '' instead of Null

  # Shirt for each club (if applicable)
  shirt_received_date   = models.DateField('Shirt received on',
                            null=True,  # Blank is stored as Null
                            blank=True) # Field is optional

  def __unicode__(self): #Python 3.3 is __str__
    return "%s --> %s"%(self.member.get_full_name(), self.club.name_short)
