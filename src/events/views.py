import json
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone

from .models import Event
from .forms import EventEditForm



# Helper functions

def round_time(dt, roundTo):
  """Round a datetime object to any time laps in seconds
  dt = datetime.datetime object
  roundTo = Closest number of seconds to round to
  """
  seconds = (dt - dt.min).seconds
  rounding = (seconds+roundTo/2) // roundTo * roundTo
  return dt + timedelta(0,rounding-seconds,-dt.microsecond)

def get_default_event_hours():
  # By default, timed events are 2 hours long
  return getattr(settings, 'EVENTS_DEFAULT_HOURS', 2)

def get_default_event_days():
  # By default, all-day events are 1 day long
  return getattr(settings, 'EVENTS_DEFAULT_DAYS', 1)




# Views

def events(request):
  context = {
    'addperm': request.user.has_perm('events.add_event'),
    'changeperm': request.user.has_perm('events.change_event'),
    'defaulthours': get_default_event_hours(),
    'defaultdays': get_default_event_days(),
  }
  return render(request, "events.html", context)



def event_view(request, eventid):
  return HttpResponse('(to be implemented)')

def event_edit(request, eventid):
  if not request.user.has_perm('events.change_event'):
    raise Http404("You do not have privileges to edit events.")

  if request.method == 'POST':
    if '_submitdelete' in request.POST:
      # User wants to delete the item
      Event.objects.get(id=eventid).delete()
      return render(request, "events_submitandrefresh.html")

    else:
      # User posted changes
      event = Event.objects.get(id=eventid)
      form = EventEditForm(request.POST, instance=event)
      if form.is_valid():
        form.instance.save()
        return render(request, "events_submitandrefresh.html")
      else:
        pass  # Show the form with the errors

  else:
    # Initial load of the form
    event = Event.objects.get(id=eventid)
    form = EventEditForm(instance=event)

  context = {
    'form': form,
    'add': False,
    'eventid': eventid,
    'is_popup': True
  }
  return render(request, "events_edit.html", context)

def event_new(request):
  if not request.user.has_perm('events.add_event'):
    raise Http404("You do not have privileges to create events.")

  if request.method == 'POST':
    # User posted changes
    form = EventEditForm(request.POST)
    if form.is_valid():
      form.instance.save()
      return render(request, "events_submitandrefresh.html")
    else:
      pass  # Show the form with the errors

  else:
    # Initial load of the form
    initialdata = {}
    st = request.GET.get('start', None)
    if st:
      try:
        initialdata['start'] = datetime.strptime(st, "%Y-%m-%dT%H:%M:%S")
        initialdata['duration'] = timedelta(hours=get_default_event_hours())
      except ValueError:
        try:
          initialdata['start'] = datetime.strptime(st, "%Y-%m-%d")
          initialdata['duration'] = timedelta(days=get_default_event_days())
          initialdata['all_day'] = True
        except ValueError:
          pass  # Leave the field blank if we cannot parse the input
    else:
      initialdata['start'] = round_time(timezone.now(), 60*60)   # Round the current time to the nearest hour
      initialdata['duration'] = timedelta(hours=get_default_event_hours())

    form = EventEditForm(initial=initialdata)

  context = {
    'form': form,
    'add': True,
    'is_popup': True
  }
  return render(request, "events_edit.html", context)



def jsonsearch(request):
  # Determine what date range to query. This is an efficient, but not correct, way of finding
  #   events within the desired range. A more correct way would be to query the database as
  #   .filter(end__gte=start, start__lte=end)
  #   But we can't do this because we don't store the end time in the database, only a duration3
  #   Rather than have SQL compute the end time as start+duration, we just use a margin factor to
  #   collect a few extra days on each end.
  margin = timedelta(days=3)
  start = datetime.strptime(request.GET["start"], "%Y-%m-%d") - margin
  end = datetime.strptime(request.GET["end"], "%Y-%m-%d") + margin

  # Query the database
  events = Event.objects.filter(start__gte=start, start__lte=end)

  # Format it for JSON
  jsondump = []
  for e in events:
    jsondump += [{
          'id': e.id,
          'title': e.title,
          'start': e.start.isoformat(),
          'end': (e.start + e.duration).isoformat(),
          'allDay': e.all_day,
          'url': '/events/%s/edit/' % e.id,
    }]
  jsondump = json.dumps(jsondump)
  return HttpResponse(jsondump, content_type='application/json')

def fcdragmodify(request):
  if not request.user.has_perm('events.change_event'):
    raise Http404("You do not have privileges to edit events.")

  e = Event.objects.get(pk=int(request.GET["id"]))
  newallday = True if (request.GET["allday"]=='true') else False
  newstart = datetime.utcfromtimestamp(float(request.GET["newstart"]))
  newend = request.GET["newend"]
  if (newend!='null'):
    # If end time is provided by fullcalendar, we will use it
    e.duration = datetime.utcfromtimestamp(float(newend)) - newstart
  else:
    if ((e.all_day == True) and (newallday == False)):
      # If user just dragged the event from the all-day section to the hourly section,
      # fullcalendar will show the event as [defaultTimedEventDuration] long, regardless of what
      # it was before, so force the database to match
      e.duration = timedelta(hours=get_default_event_hours())
    elif ((e.all_day == False) and (newallday == True)):
      # If user just dragged the event from the hourly section to the all-day section,
      # fullcalendar will show the event on only one day, even if it was a multi-day event before.
      # So force the database to match this behavior.
      e.duration = timedelta(days=get_default_event_days())
  e.start = newstart
  e.all_day = newallday
  e.save()

  return HttpResponse('ok')
