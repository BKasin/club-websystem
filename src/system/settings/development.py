from .base import *
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# Debug mode will help troubleshoot errors
DEBUG = True

# Custom settings for dynamically-generated config files
PROJECT_NAME = PROJECT_NAME+'-development'

# Must have some key, so we'll just use bogus one
SECRET_KEY = '00000000000000000000000000000000000000000000000000'


# Database backend(s)
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(DATA_DIR, 'development.sqlite3'),
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

# Specify the domain names Django will respond to
ALLOWED_HOSTS = [
  'localhost', '127.0.0.1',   # Access from same machine
  '192.168.0.26', '192.168.224.102',  # Development virtual machine
]

# Since manage.py runserver does not understand the static files layout we
# use at production (static files and django served out of the same root, but using
# nginx's try_files to distinguish), we must use the /static prefix when using
# django's development server
STATIC_URL = '/static/'

############################################## Misc. ###############################################
