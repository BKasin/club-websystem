#####################################################
#
# Example of a s_50_production_club.py settings file
#
#####################################################

import os
from django.conf import settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: never allow this key to be stored in any source control (GitHub)!
# Production key
SECRET_KEY = 'uagpxd6=rb0ib5-(k*stqbw&vdsgrhq71lhv_z)*ie=&z@aj94'  # not a real one; this is just for simulation

# Production database settings
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
  }
}

# Keep database connections alive for X seconds, for extra speed
# This applies to each thread (uWSGI worker), so ensure the database
# supports as many simultaneous connections as there are worker threads
CONN_MAX_AGE = 300

# Mark cookies as 'secure', to tell browsers to only send over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Make django cache the templates to increase speed (still testing this one; not ready for production yet)
# settings.TEMPLATES[0]['OPTIONS']['loaders'] = [
#   ('django.template.loaders.cached.Loader', [
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#   ]),
# ]
# del settings.TEMPLATES[0]['APP_DIRS']

# Email settings
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = '"Information Security Club" <support@infosec-csusb.org>'
GENERIC_CONTACT_EMAIL = ['csusb.infosec.club@gmail.com']

# Restrict connections to a list of hosts
ALLOWED_HOSTS = [
  'www.infosec-csusb.org'
]

# Settings for django.sites
SITE_ID = 8001

# Look in the club-specific template folder first
settings.TEMPLATES[0]['DIRS'].insert(0, os.path.join(settings.BASE_DIR, "templates", 'infosec'))