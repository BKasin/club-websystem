import os
from django.conf import settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Send to the local debug smpt server.
# Start it by running this in a terminal:
#   python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025

# Keep track of which club we're in
CURRENT_CLUB_ID = 1   # primary key of the club in the database
CURRENT_CLUB = 'infosec'

# Insert the club's template directory at the beginning, so it will
# take precedence over the root template directory
settings.TEMPLATES[0]['DIRS'] = [
  os.path.join(settings.BASE_DIR, "templates", CURRENT_CLUB),
] + settings.TEMPLATES[0]['DIRS']
