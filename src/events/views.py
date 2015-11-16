from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Event
import json
from datetime import datetime, timedelta

# Method #1: multiple event sources
CALSOURCES = """
    googleCalendarApiKey: 'AIzaSyDKSBh7lXk8DS8TASIywg6E2JD8ZvGA9Lo',
    eventSources: [
      {
        url: "/events/json/",
        className: 'calitem_blue'
      },
      {
        googleCalendarId: 'csusb.infosec.club@gmail.com',
        className: 'calitem_red'
      }
    ]
"""

# Method #2: single event source
'''CALSOURCES = """
    events: {
        url: "/events/json/",
        className: 'calitem_blue'
    }
"""'''

def events(request):
  context = {
    'calendar_config_options': CALSOURCES
  }
  return render(request, "events.html", context)

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
    print(type(e.start))
    jsondump += [{
          'id': e.id,
          'title': e.title,
          'start': e.start.isoformat(),
          'end': (e.start + e.duration).isoformat(),
          'allDay': e.all_day,
          'url': '/events/edit/%s/' % e.id,
    }]
  jsondump = json.dumps(jsondump)
  return HttpResponse(jsondump, content_type='application/json')

def eventmodify(request):
  e = Event.objects.get(pk=int(request.GET["id"]))
  newallday = True if (request.GET["allday"]=='true') else False
  newstart = datetime.utcfromtimestamp(float(request.GET["newstart"]))
  newend = request.GET["newend"]
  if (newend=='null'):
    if ((e.all_day == True) and (newallday == False)):
      # If user just dragged the event from the all-day section to the hourly section,
      # fullcalendar will show the event as 2 hours long, regardless of what it was before,
      # so force the database to match
      e.end = newstart + timedelta(hours=2)
    elif ((e.all_day == False) and (newallday == True)):
      # If user just dragged the event from the hourly section to the all-day section,
      # fullcalendar will show the event as 1 day long, regardless of what it was before,
      # so force the database to match
      e.end = newstart + timedelta(days=1)
    else:
      # Sometimes, fullcalendar just fails to give us the end time, so we must calculate it
      e.end = (e.end - e.start) + newstart
  else:
    # If end time is provided by fullcalendar, we will use it
    e.end = datetime.utcfromtimestamp(float(newend))
  e.start = newstart
  e.all_day = newallday
  e.save()

  return HttpResponse('ok')
