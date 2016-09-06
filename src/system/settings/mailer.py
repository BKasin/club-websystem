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
]


############################################# Database #############################################

# Database backend(s)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),
  }
}


############################################## Email ###############################################

# Configure django-mailer as the primary backend, and configure it to use our original backend
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_BACKEND = 'mailer.backend.DbBackend'


############################################### Site ###############################################

############################################### URLs ###############################################

############################################## Misc. ###############################################
