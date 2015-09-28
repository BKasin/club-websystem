import os
from django.conf import settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Development key only
SECRET_KEY = 'uagpxd6=rb0ib5-(k*stqbw&vdsgrhq71lhv_z)*ie=&z@aj94'

# Development database settings
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
  }
}

# Since manage.py runserver does not understand the static files layout we
# use at production (static files and django served out of the same root, but using
# nginx's try_files to distinguish), we must use the /static prefix when using
# django's development server
STATIC_URL = '/static/'

# Keep track of which club we're in
CURRENT_CLUB_ID = 1   # primary key of the club in the database
CURRENT_CLUB = 'infosec'
settings.TEMPLATES[0]['DIRS'].insert(0, os.path.join(settings.BASE_DIR, "templates", CURRENT_CLUB))

# Send to the local debug smpt server.
# Start it by running this in a terminal: python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025
