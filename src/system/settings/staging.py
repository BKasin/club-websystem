"""
Staging for the InfoSec website. For staging, we're using a virtual machine that does not have an
SSL cert. So we'll import from the production settings file, and just tweak things to make it work.
"""

from ._production_infosec import *
import os
print("  + settings/%s" % os.path.basename(os.path.abspath(__file__)))

# Redirect to a local copy of the production database
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'staging.sqlite3'),
  }
}

# Allow our virtual machine's host name
ALLOWED_HOSTS = ['www.test-club.org']

# Since we don't have an SSL cert for the VM, turn these settings off
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
