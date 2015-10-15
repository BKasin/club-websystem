"""
Settings file for use in development only.
"""

from .base import *
import os
print("  + settings/%s" % os.path.basename(os.path.abspath(__file__)))


############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# List all remote IPs you will use to access the website for dev purposes
# This allows django.template.context_processors.debug to work
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

# Secret key used for cryptographic signing of sessions, password reset tokens, etc.
# SECURITY WARNING: never allow this key to be stored in any source control (GitHub)!
SECRET_KEY = '00000000000000000000000000000000000000000000000000'


############################################# Modules ##############################################

# Add our own apps to the ones defined by the base settings
INSTALLED_APPS += [
  'clubdata',
  'clubmembers',
  'contentblocks',
  'events',
  'mainsite_acm',
  'regbackend',
  'transactionalemail',
]

# Look in the club-specific template folder first
TEMPLATES[0]['DIRS'].insert(0,
  os.path.join(BASE_DIR, "templates", 'acm')
)


############################################# Database #############################################

# Database backend(s)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}


############################################## Email ###############################################

# Email server to send outbound mail
# This uses Python's built-in development SMTP server; start it by running this in a terminal:
#     python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025

# All outbound email will have this as the From: header, unless overridden
DEFAULT_FROM_EMAIL = '"Test Club" <support@test-club.org>'

# Messages submitted through the contact page will be sent to these addresses
GENERIC_CONTACT_EMAIL = ['test-club@gmail.com']


############################################### Site ###############################################

# Settings for django.sites
SITE_ID = 8002


############################################### URLs ###############################################

# Load the initial urlconf
ROOT_URLCONF = 'system.urls.acm'

# Since manage.py runserver does not understand the static files layout we
# use at production (static files and django served out of the same root, but using
# nginx's try_files to distinguish), we must use the /static prefix when using
# django's development server
STATIC_URL = '/static/'

############################################## Misc. ###############################################
