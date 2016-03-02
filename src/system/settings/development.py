"""
Settings file for use in development only.
"""

from .base import *
import os


############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# List all remote IPs you will use to access the website for dev purposes
# This allows django.template.context_processors.debug to work
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

# Secret key used for cryptographic signing of sessions, password reset tokens, etc.
# SECURITY WARNING: Load it from an external file, so the actual key never gets stored in the git repo or GitHub!
from .SECRETKEY import SECRET_KEY


############################################# Modules ##############################################

# Add our own apps to the ones defined by the base settings
INSTALLED_APPS += [
  'clubdata',
  'clubmembers',
  'contentblocks',
  'events',
  'mainsite',
  'regbackend',
]


############################################# Database #############################################

# Database backend(s)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}


############################################## Email ###############################################

# Pretend email server for development use
if True:
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
  EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
  EMAIL_FILE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'emails_filebased')

# All outbound email will have this as the From: header, unless overridden
DEFAULT_FROM_EMAIL = '"Test Club" <support@test-club.org>'

# Messages submitted through the contact page will be sent to these addresses
GENERIC_CONTACT_EMAIL = ['test-club@gmail.com']


############################################### Site ###############################################

# Settings for django.sites
SITE_ID = 8001


############################################### URLs ###############################################

# Since manage.py runserver does not understand the static files layout we
# use at production (static files and django served out of the same root, but using
# nginx's try_files to distinguish), we must use the /static prefix when using
# django's development server
STATIC_URL = '/static/'

############################################## Misc. ###############################################
