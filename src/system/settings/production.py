from .base import *
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# Custom settings for dynamically-generated config files
UWSGI_PORT = 9001
HTTP_PORT = 80
HTTPS_PORT = 443
HTTPS_ENABLED = True

############################################## Basics ##############################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Import key from an external file, so it doesn't get included in version control
SECRET_KEY_FILE = os.path.join(CONF_DIR, 'secretkey.txt')
try:
  with open(SECRET_KEY_FILE, 'r') as f:
    SECRET_KEY = f.read().strip()
except:
  SECRET_KEY = '*** NOT CONFIGURED ***'
  print("WARNING: the SECRET_KEY setting has not yet been configured!")


# Restrict host/domain names
ALLOWED_HOSTS = ['www.' + DOMAIN_NAME]

############################################# Modules ##############################################

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
# creds_file = open(os.path.join(CONF_DIR, 'dbcreds.txt'))
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(DATA_DIR, 'production.sqlite3'),
  }
  # 'default': {
  #   'ENGINE': 'django.db.backends.mysql',
  #   'NAME': 'sampledb',
  #   'USER': creds_file.readline().strip(),
  #   'PASSWORD': creds_file.readline().strip(),
  #   'HOST': '127.0.0.1',
  #   'PORT': '5432',
  # },
}
# creds_file.close()

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
ALLOWED_HOSTS = ['www.infosec-csusb.org']


############################################## Misc. ###############################################

# Mark cookies as 'secure', to tell browsers to only send over HTTPS
if HTTPS_ENABLED:
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
