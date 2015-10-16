"""
Example of a production settings file.
More information can be found in Django's Deployment Checklist:
https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
"""

from .base import *
import os
print("  + settings/%s" % os.path.basename(os.path.abspath(__file__)))


############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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
  'mainsite_infosec',
  'regbackend',
]

# Look in the club-specific template folder first
TEMPLATES[0]['DIRS'].insert(0,
  os.path.join(BASE_DIR, "templates", 'infosec')
)

# Make django cache the templates to increase speed (still testing this one; not ready for production yet)
# TEMPLATES[0]['OPTIONS']['loaders'] = [
#   ('django.template.loaders.cached.Loader', [
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#   ]),
# ]
# del TEMPLATES[0]['APP_DIRS']


############################################# Database #############################################

# Database backend(s)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'system',
    'USER': 'username',
    'PASSWORD': '000000000000000000000000000000000',
    'HOST': 'localhost',
    'PORT': '',
  }
}

# Keep database connections alive for X seconds, for extra speed
# This applies to each thread (uWSGI worker), so ensure the database
# supports as many simultaneous connections as there are worker threads
CONN_MAX_AGE = 300


############################################## Email ###############################################

# Email server to send outbound mail
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25

# All outbound email will have this as the From: header, unless overridden
DEFAULT_FROM_EMAIL = '"Information Security Club" <support@infosec-csusb.org>'

# Messages submitted through the contact page will be sent to these addresses
GENERIC_CONTACT_EMAIL = ['csusb.infosec.club@gmail.com']


############################################### Site ###############################################

# Settings for django.sites
SITE_ID = 8001


############################################### URLs ###############################################

# Restrict connections to a list of hosts (required if DEBUG=False)
ALLOWED_HOSTS = ['www.infosec-csusb.org']

# Load the initial urlconf
ROOT_URLCONF = 'system.urls.infosec'


############################################## Misc. ###############################################

# Mark cookies as 'secure', to tell browsers to only send over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
