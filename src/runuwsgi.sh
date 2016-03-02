#!/bin/sh

if [ "$VIRTUAL_ENV" = "" ]; then
  echo "No virtual environment found"
  exit
fi

settingsfile="_production"
if [ $# -gt 0 ]; then
  if [ "$1" = "-s" ]; then
    settingsfile=${2%.py}
  fi
else
  echo "Usage: $0 [-s settingsfile]"
  echo "Defaulting to $0 -s $settingsfile"
fi

if [ -f "$VIRTUAL_ENV/src/system/settings/$settingsfile.py" ]; then
  if [ -f "$VIRTUAL_ENV/src/system/settings/$settingsfile.ini" ]; then
    export DJANGO_SETTINGS_MODULE="system.settings.$settingsfile"

    r="uwsgi --ini $VIRTUAL_ENV/src/system/settings/$settingsfile.ini"
    echo "DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE"
    echo $r
    echo ------------------------------------
    $r
  else
    echo "Cannot find UWSGI file named '$settingsfile.ini'"
  fi
else
  echo "Cannot find settings file named '$settingsfile.py'"
fi
