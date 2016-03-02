#!/bin/sh

if [ "$VIRTUAL_ENV" = "" ]; then
  echo "No virtual environment found"
  exit
fi

command="runserver 0.0.0.0:8000"
settingsfile="development"
if [ $# -gt 0 ]; then
  if [ "$1" = "-s" ]; then
    settingsfile=${2%.py}
    shift
    shift
  fi
  if [ $# -gt 0 ]; then
    command="$*"
  else
    echo "No command specified; defaulting to $0 -s $settingsfile $command"
  fi
else
  echo "Usage: $0 [-s settingsfile] [command]"
  echo "Defaulting to $0 -s $settingsfile $command"
fi

if [ -f "$VIRTUAL_ENV/src/system/settings/$settingsfile.py" ]; then
  export DJANGO_SETTINGS_MODULE="system.settings.$settingsfile"

  r="$VIRTUAL_ENV/bin/python $VIRTUAL_ENV/src/manage.py $command"
  echo "DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE"
  echo $r
  echo ------------------------------------
  $r
else
  echo "Cannot find settings file named '$settingsfile.py'"
fi
