#!/bin/sh

# Uses django-mailer to periodically send out the scheduled/deferred emails.
# Since this is club-neutral, we use our own minimal settings file.

scriptdir=$(dirname $0)
log=$scriptdir/mailer.log
if [ $# -gt 0 ]; then
  # Activate the virtual environment
  . $scriptdir/../bin/activate

  # Write a header to the log
  (echo -ne "\n\n------------------------------------------------------------------------\n$1 - "; date; [ "$1" != "send_mail" ] && echo "------------------------------------------------------------------------") >> $log

  # Run the mailer tool
  export DJANGO_SETTINGS_MODULE="system.settings.mailer"
  python $VIRTUAL_ENV/src/manage.py $* >> $log 2>&1
else
  echo "You must specify one parameter: either send_mail or retry_deferred"
fi
