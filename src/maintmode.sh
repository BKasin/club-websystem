#!/bin/sh

if [ "$VIRTUAL_ENV" = "" ]; then
  echo "No virtual environment found"
  exit
fi

maintfile="$VIRTUAL_ENV/static_in_env/static_root/maint.html"

if [ $# -gt 0 ]; then
  [ -f "$maintfile" ] && maintmode="ON" || maintmode="OFF"
  if [ $1 = "off" ]; then
    if [ "$maintmode" = "ON" ]; then
      echo "Disabling $maintfile..."
      mv ${maintfile} ${maintfile}.disabled || exit
    fi
  elif [ $1 = "on" ]; then
    if [ "$maintmode" = "OFF" ]; then
      if [ -f "${maintfile}.disabled" ]; then
        echo "Enabling $maintfile..."
        mv ${maintfile}.disabled ${maintfile} || exit
      else
        echo "Creating $maintfile..."
        echo "This website is temporarily in maintenance mode" > ${maintfile} || exit
      fi
    fi
  else
    echo "Usage:"
    echo "$0 [on | off]"
    exit
  fi
fi

[ -f "$maintfile" ] && maintmode="ON" || maintmode="OFF"
echo "Current maintenance mode status: $maintmode"
