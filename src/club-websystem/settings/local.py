# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Send to the local debug smpt server.
# Start it by running this in a terminal:
#   python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = 'kenpilot@gmail.com'
