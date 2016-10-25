from .production import *
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# Custom settings for dynamically-generated config files
PROJECT_NAME = PROJECT_NAME+'-staging'
UWSGI_PORT = 9002
HTTP_PORT = 81
HTTPS_PORT = 444

# Redirect to a local copy of the production database
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(DATA_DIR, 'staging.sqlite3'),
  }
}
