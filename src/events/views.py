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
        url: "/eventjson/",
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
        url: "/eventjson/",
        className: 'calitem_blue'
    }
"""'''

def calendar(request):
  context = {
    'calendar_config_options': CALSOURCES
  }
  return render(request, "calendar.html", context)

def eventjson(request):
  # Determine what date range to query
  start = datetime.strptime(request.GET["start"], "%Y-%m-%d")
  end = datetime.strptime(request.GET["end"], "%Y-%m-%d")

  # Query the database
  events = Event.objects.filter(end__gte=start).filter(start__lte=end)

  # Format it for JSON
  events_values = list(events.values('id', 'title', 'start', 'end', 'allDay'))
  jsondump = json.dumps(events_values,
      default=lambda obj: obj.isoformat() if hasattr(obj, 'isoformat') else obj)

  return HttpResponse(jsondump, content_type='application/json')

def eventmodify(request):
  e = Event.objects.get(pk=int(request.GET["id"]))
  newallday = True if (request.GET["allday"]=='true') else False
  newstart = datetime.utcfromtimestamp(float(request.GET["newstart"]))
  newend = request.GET["newend"]
  if (newend=='null'):
    if ((e.allDay == True) and (newallday == False)):
      # If user just dragged the event from the all-day section to the hourly section,
      # fullcalendar will show the event as 2 hours long, regardless of what it was before,
      # so force the database to match
      e.end = newstart + timedelta(hours=2)
    elif ((e.allDay == False) and (newallday == True)):
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
  e.allDay = newallday
  e.save()

  return HttpResponse('ok')
