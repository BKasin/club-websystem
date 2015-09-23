# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.alofoxx.com',  # Allow domain and subdomains
    '.alofoxx.com.',  # Also allow FQDN and subdomains
]

# Send to the local debug smpt server.
# Start it by running this in a terminal:
#   python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = 'kenpilot@gmail.com'

# Keep track of which club we're in
CURRENT_CLUB_ID = 1   # primary key of the club in the database
CURRENT_CLUB = 'infosec'

# Insert the club's template directory at the beginning, so it will
# take precedence over the root template director
import os
from .base import TEMPLATES, BASE_DIR
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, "templates", CURRENT_CLUB)] + TEMPLATES[0]['DIRS']
