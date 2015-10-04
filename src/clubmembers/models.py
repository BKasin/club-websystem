import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.backends import ModelBackend
from django.core import validators
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnDiscPlaceholderImage

from clubdata.models import Club


validate_username = validators.RegexValidator(r'^[\w.@+-]+$')  # Letters, digits or @.+-_
validate_coyoteid = validators.RegexValidator(r'^[\d]+$')  # Numbers only

class MemberAuthenticationBackend(ModelBackend):
  # Extends Django's default authentication backend, for use with our custom
  # Member model. Changes only one thing: allows the user to login with fields
  # other than just username

  def authenticate(self, username=None, password=None):
    try:
      user = Member._default_manager.get(**{'username': username})
      if user.check_password(password):
        return user
    except Member.DoesNotExist:
      try:
        user = Member._default_manager.get(**{'email': username})
        if user.check_password(password):
          return user
      except Member.DoesNotExist:
        try:
          user = Member._default_manager.get(**{'coyote_id': username})
          if user.check_password(password):
            return user
        except Member.DoesNotExist:
          # We've been unable to find the user, but before we return None,
          # run the default password hasher once to add the same timing delay
          # there would have been had we found the user and checked the password
          # See the security vulnerability info at
          # https://code.djangoproject.com/ticket/20760
          Member().set_password(password)

class MemberManager(BaseUserManager):
  # Custom manager object for the Member model below

  def create_user(self, username, email, password=None):
    """
    Creates and saves a Member with the given email, date of
    birth and password.
    This method should have the same parameters as create_superuser below,
    but allows the password to be left out.
    """
    if not username:
      raise ValueError('Members must have a username')

    user = self.model(
      username=username,
      email=self.normalize_email(email)
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, email, password):
    """
    Called by 'python manage.py createsuperuser to creates a user that
    gets all privileges without being specifically set.
    This method will receive username, followed by any fields specified below
    in REQUIRED_FIELDS, then followed by the password.
    It should use the create_user method above to create the Member, and then
    modify that user to make it a superuser.
    """
    user = self.create_user(
      username=username,
      email=email,
      password=password
    )
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self._db)
    return user

class Member(AbstractBaseUser, PermissionsMixin):
  # AbstractBaseUser will add the following fields:
  # password            = models.CharField(...)
  # last_login          = models.DateTimeField(...)

  # PermissionsMixin will add the following fields:
  # is_superuser        = models.BooleanField(...)
  # groups              = models.ManyToManyField(Group, ...)
  # user_permissions    = models.ManyToManyField(Permission, ...)

  is_active             = models.BooleanField('Account activated?',
                            default=True)
  is_staff              = models.BooleanField('May login to /admin?',
                            default=False)
  date_created          = models.DateTimeField('Date created',
                            default=timezone.now,
                            editable=False)
  username              = models.CharField('User name',
                            help_text='Letters, digits or the following symbols only: <span style="font-size:1.2em">@.+-_</span>',
                            max_length=50,
                            unique=True, # Two members cannot use the same username
                            validators=[validate_username],
                            error_messages={'unique': "Another InfoSec Club member with that username already exists.",})
  coyote_id             = models.CharField('Coyote ID #',
                            help_text='Provide the 9-digit CSUSB student identification number. Leave blank if member is not yet or no longer a student.',
                            max_length=9,
                            #unique=True, # Since the field is optional, we cannot require it to be unique
                            blank=True, # Field is optional, but blank is stored as '' instead of Null
                            validators=[validate_coyoteid])
  name_first            = models.CharField('First name',
                            max_length=30)
  name_last             = models.CharField('Last name',
                            max_length=30)

  # Contact info
  email                 = models.EmailField('Email address',
                            unique=True) # Two members cannot use the same email
  email_pending         = models.EmailField('Pending email address',
                            help_text='This field is only to be used for an email that has not yet been verified by the user. Once verified, the <i>email</i> field is updated and this one is cleared.',
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  phone                 = models.CharField('Phone number',
                            help_text='Please enter your phone number in the following format: 000-000-0000',
                            max_length=100, # Extra long to allow notes after the number
                            blank=True) # Field is optional, but blank is stored as '' instead of Null
  texting_ok            = models.BooleanField('SMS Okay?',
                            help_text='May the club send SMS messages to this number? Your usual SMS charges will still apply.',
                            default=True)

  # Photo of user
  photo                 = VersatileImageField('Profile photo',
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
                            max_length=128,
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

  # Define custom manager class
  objects = MemberManager()

  # Field which will act as username field
  USERNAME_FIELD = 'username'

  # Fields required when using 'python manage.py createsuperuser'. Doesn't affect
  # any other part of Django. See the create_superuser method in MemberManager above
  REQUIRED_FIELDS = ['email']

  def get_short_name(self):
    return self.name_first

  def get_full_name(self):
    return " ".join((self.name_first, self.name_last))

  def __unicode__(self): #Python 3.3 is __str__
    return "%s %s <%s>"%(self.name_first, self.name_last, self.username)












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
