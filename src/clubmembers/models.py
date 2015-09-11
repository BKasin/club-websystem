from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField

# Create your models here.

class Club(models.Model):
  id                    = models.AutoField(primary_key=True)
  name_short            = models.CharField(max_length=20)
  name_long             = models.CharField(max_length=120)

  def __unicode__(self): #Python 3.3 is __str__
    return self.name_short


class Member(models.Model):
  # Extends the built-in User model
  user                  = models.OneToOneField(User, primary_key=True)

  # Contact info
  phone                 = models.CharField(max_length=10, blank=True)
  texting_ok            = models.BooleanField()

  # Photo of user
  photo                = VersatileImageField(upload_to="memberphotos", width_field="photowidth", height_field="photoheight", ppoi_field="photoppoi", blank=True, default="")
  photowidth           = models.PositiveIntegerField(null=True, editable=False)
  photoheight          = models.PositiveIntegerField(null=True, editable=False)
  photoppoi            = PPOIField(blank=True, editable=False)

  # PIN number, used for signing in and out for meetings without requiring the user's full password
  pin_hash              = models.CharField(max_length=120, blank=True)

  # Other information we may be interested in
  shirt_size            = models.CharField(max_length=2, blank=True)
  acad_major            = models.CharField(max_length=50, blank=True)
  acad_minor            = models.CharField(max_length=50, blank=True)
  acad_concentration    = models.CharField(max_length=50, blank=True)
  acad_grad_qtr         = models.CharField(max_length=20, blank=True)  # Format as "<qtr> <year>" without abbreviations. ex: "Spring 2015"

  def __unicode__(self): #Python 3.3 is __str__
    return "%s %s <%s>"%(self.user.first_name, self.user.last_name, self.user.email)


class Membership(models.Model):
  id                    = models.AutoField(primary_key=True)

  # Which member is a member of which club
  member                = models.ForeignKey(Member)
  club                  = models.ForeignKey(Club)

  # Membership dues
  paid_date             = models.DateField(null=True)
  paid_until_date       = models.DateField(null=True)
  paid_amount           = models.DecimalField(max_digits=6, decimal_places=2, null=True)
  receipt_date          = models.DateField(null=True)

  # Club badges (if applicable)
  badge_type            = models.CharField(max_length=20, null=True)
  badge_issue_date      = models.DateField(null=True)

  # Shirt for each club (if applicable)
  shirt_received_date   = models.DateField(null=True)

  def __unicode__(self): #Python 3.3 is __str__
    return "%s --> %s"%(self.member.user.get_full_name, self.club.name_short)
