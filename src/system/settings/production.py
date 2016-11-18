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
SECRET_KEY_FILE = os.path.join(CONF_DIR, 'secret', 'secretkey.txt')
try:
  with open(SECRET_KEY_FILE, 'r') as f:
    SECRET_KEY = f.read().strip()
except:
  SECRET_KEY = '*** NOT CONFIGURED ***'
  print("WARNING: the SECRET_KEY setting has not yet been configured!")


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

# All mail will be queued with django-mailer instead of sent right away
EMAIL_BACKEND = 'mailer.backend.DbBackend'

# Configure django-mailer to use the original backend when manage.py send_mail is called
MAILER_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Forward emails through postfix installed on the same server
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25


############################################### URLs ###############################################

# Specify the domain names Django will respond to
ALLOWED_HOSTS = [
  'www.' + DOMAIN_NAME,
  DOMAIN_NAME,  # This one is required for PREPEND_WWW to work
]

# If the domain name doesn't start with "www." then add it
PREPEND_WWW = True


############################################## Misc. ###############################################

# Mark cookies as 'secure', to tell browsers to only send over HTTPS
if HTTPS_ENABLED:
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
