"""
Staging file for the Information Security Club's website at http://www.infosec-csusb.org,
for the purpose of testing out the production settings in a virtual machine before pushing to the
production server.
This file is identical to the production settings file, except where marked with <TEMPCHANGE>
"""

from .base import *
import os


############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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

  'quiz',
  'multichoice',
  'true_false',
  'essay',
]

# Make django cache the templates to increase speed (still testing this one; not ready for production yet)
# TEMPLATES[0]['OPTIONS']['loaders'] = [
#   ('django.template.loaders.cached.Loader', [
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#   ]),
# ]
# del TEMPLATES[0]['APP_DIRS']


############################################# Database #############################################

# Redirect to a local copy of the production database
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),
  }
}

# Keep database connections alive for X seconds, for extra speed
# This applies to each thread (uWSGI worker), so ensure the database
# supports as many simultaneous connections as there are worker threads
CONN_MAX_AGE = 300


############################################## Email ###############################################

# Configure django-mailer as the primary backend, and configure it to use our original backend
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_BACKEND = 'mailer.backend.DbBackend'

# All outbound email will have this as the From: header, unless overridden
DEFAULT_FROM_EMAIL = '"Information Security Club" <support@infosec-csusb.org>'

# Messages submitted through the contact page will be sent to these addresses
GENERIC_CONTACT_EMAIL = ['csusb.infosec.club@gmail.com']


############################################### Site ###############################################

# Settings for django.sites
SITE_ID = 8001


############################################### URLs ###############################################

# Restrict connections to a list of hosts (required if DEBUG=False)
#ALLOWED_HOSTS = ['www.infosec-csusb.org']
ALLOWED_HOSTS = ['www.test-club.org']   # <TEMPCHANGE>,  /etc/hosts override on staging server


############################################## Misc. ###############################################

# Mark cookies as 'secure', to tell browsers to only send over HTTPS
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False      # <TEMPCHANGE>, no SSL on staging server
SESSION_COOKIE_SECURE = False   # <TEMPCHANGE>, no SSL on staging server
