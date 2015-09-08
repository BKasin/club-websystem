from django.conf import settings
from django.db import models
from django.utils import timezone

class Club(models.Model):
  id                    = models.AutoField(primary_key=True)

  name_short            = models.CharField(max_length=20)
  name_long             = models.CharField(max_length=120)

  def __unicode__(self): #Python 3.3 is __str__
    return self.name_short


class Member(models.Model):
  # Extends the built-in User model
  user                  = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

  phone                 = models.CharField(max_length=10, null=True)
  texting_ok            = models.BooleanField()

  MALE = 'M'
  FEMALE = 'F'
  gender                = models.CharField(max_length=1, null=True, choices=((MALE, 'Male'), (FEMALE, 'Female')))

  pin_hash              = models.CharField(max_length=120, null=True)

  shirt_size            = models.CharField(max_length=2, null=True)

  acad_major            = models.CharField(max_length=50, null=True)
  acad_minor            = models.CharField(max_length=50, null=True)
  acad_concentration    = models.CharField(max_length=50, null=True)
  acad_grad_qtr         = models.CharField(max_length=20, null=True)

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
    return "%s %s --> %s"%(self.member.user.first_name, self.member.user.last_name, self.club.name_short)
