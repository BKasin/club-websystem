"""
Base settings module. Not meant to be used alone.

Each website should have their own settings file under system/settings,
which imports from base:
  from .base import *

In development, set the appropriate settings file like this:
  export DJANGO_SETTINGS_MODULE='system.settings.yourfilehere'
  python manage.py runserver 0.0.0.0:8000

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
def get_file_name_only(path):
  return os.path.splitext(os.path.basename(path))[0]
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# To ensure everything will work on both Linux and Windows, build paths
# inside your the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Custom settings
CONF_DIR = os.path.join(os.path.dirname(BASE_DIR), 'conf')
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
PROJECT_NAME = 'infosec'
DOMAIN_NAME = 'infosec-csusb.org'


############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Secret key used for cryptographic signing of sessions, password reset tokens, etc.
# SECURITY WARNING: never allow this key to be stored in any source control (GitHub)!
#SECRET_KEY = '' # You must define this in your custom settings file


############################################# Modules ##############################################

# Application definition
INSTALLED_APPS = [
  # our core (list it first, so we have complete authority to override templates and static files in other apps)
  'system',

  # simple management commands
  'django_rotate_secret_key',
  'django_maint_mode_toggle',
  'django_generate_dynamic_configs',

  # bootstrap the admin (must be before django.contrib.admin)
  'django_admin_bootstrapped',

  # django
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.sites',
  'django.contrib.staticfiles',

  # third party apps
  'crispy_forms',
  'registration',
  'versatileimagefield',
  'mailer',

  # our apps
  'clubdata',
  'clubmembers',
  'membership',
  'contentblocks',
  'events',
  'regbackend',
  'quiz',
  'multichoice',
  'true_false',
  'essay',
]

# Middleware
MIDDLEWARE_CLASSES = [
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',
]

# Templates
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]


############################################# Database #############################################

# Custom user model
AUTH_USER_MODEL = 'clubmembers.Member'
AUTHENTICATION_BACKENDS = ('clubmembers.models.MemberAuthenticationBackend',)


############################################## Email ###############################################

# All outbound email will have this as the From: header, unless overridden
DEFAULT_FROM_EMAIL = '"Information Security Club" <support@' + DOMAIN_NAME + '>'

# Use the same email for error messages sent to admins specified in ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Messages submitted through the contact page will be sent to these addresses
GENERIC_CONTACT_EMAIL = ['csusb.infosec.club@gmail.com']

# People who should receive error notifications
ADMINS = (
  ('Kenneth', 'kenpilot@gmail.com'),
)
MANAGERS = ADMINS


############################################### Site ###############################################

# Settings for django.sites
SITE_ID = 8001


############################################### URLs ###############################################

# Load the initial urlconf
ROOT_URLCONF = 'system.urls'

# Static files (CSS, JavaScript, Images). Because we're using try_files
# in nginx, we serve static content from the same URI root that the pages
# are in. For development, we can override this with '/static/'.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, "static")

# Media files (untrusted files uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, "media")

# Django auth settings
LOGIN_REDIRECT_URL = '/'


################################# Registration and Authentication ##################################

#DJANGO REGISTRATION REDUX SETTINGS
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 14

# Settings for our pending email function in the clubmembers app
PENDINGEMAIL_CONFIRMATION_DAYS = 14


####################################### Internationalization #######################################

# Do not use any language translation features
USE_I18N = False

# Do not format numbers and dates using the system locale
USE_L10N = False

# Project is in the Pacific timezone, but will use timezone-unaware dates internally
TIME_ZONE = 'America/Los_Angeles'
USE_TZ = False

# Default date format when displaying dates in templates
DATE_FORMAT = 'N j, Y'                  #ex: Feb. 4, 2003
DATETIME_FORMAT = 'N j, Y, g:i A'       #ex: Feb. 4, 2003, 4:13 PM
TIME_FORMAT = 'g:i A'                   #ex: 4:13 PM
MONTH_DAY_FORMAT = 'F j'                #ex: January 4
YEAR_MONTH_FORMAT = 'F Y'               #ex: January 2003
SHORT_DATE_FORMAT = 'm/d/Y'             #ex: 12/31/2003
SHORT_DATETIME_FORMAT = 'm/d/Y g:i A'   #ex: 12/31/2003 4:13 PM

# Customize the input formats to prefer the seconds hidden
DATETIME_INPUT_FORMATS = (
  '%Y-%m-%d %H:%M',         # '2006-10-25 14:30'
  '%Y-%m-%d %H:%M:%S',      # '2006-10-25 14:30:59'
  '%Y-%m-%d %H:%M:%S.%f',   # '2006-10-25 14:30:59.000200'
  '%Y-%m-%d',               # '2006-10-25'
  '%m/%d/%Y %H:%M',         # '10/25/2006 14:30'
  '%m/%d/%Y %H:%M:%S',      # '10/25/2006 14:30:59'
  '%m/%d/%Y %H:%M:%S.%f',   # '10/25/2006 14:30:59.000200'
  '%m/%d/%Y',               # '10/25/2006'
  '%m/%d/%y %H:%M',         # '10/25/06 14:30'
  '%m/%d/%y %H:%M:%S',      # '10/25/06 14:30:59'
  '%m/%d/%y %H:%M:%S.%f',   # '10/25/06 14:30:59.000200'
  '%m/%d/%y',               # '10/25/06'
)
TIME_INPUT_FORMATS = (
  '%H:%M',                  # '14:30'
  '%H:%M:%S',               # '14:30:59'
  '%H:%M:%S.%f',            # '14:30:59.000200'
)

############################################## Misc. ###############################################

# Customize the CSS classses for the django.contrib.messages framework
from django.contrib import messages
MESSAGE_TAGS = {
  messages.INFO: 'alert-info',
  messages.SUCCESS: 'alert-success',
  messages.WARNING: 'alert-warning',
  messages.ERROR: 'alert-danger'
}

# Settings for django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = True

# Settings for django-versatileimagefield
VERSATILEIMAGEFIELD_SETTINGS = {
  'cache_length': 2592000,
  'cache_name': 'versatileimagefield_cache',
  'jpeg_resize_quality': 70,
  # Separate auto-generated images from the originals
  'sized_directory_name': 'sized',
  'filtered_directory_name': 'filtered',
  # Placeholder images have their own subdirectory: sized/placeholder or filtered/placeholder
  'placeholder_directory_name': 'placeholders',
  # Do not create any images on demand. That way, we don't have page errors due to missing images.
  # No need to create these on demand, since they are created on the post-save event of Member
  'create_images_on_demand': False,
}
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
  'memberphoto': [
    ('menu_icon', 'thumbnail__20x20'),
    ('profile_page', 'thumbnail__100x100'),
  ],
}