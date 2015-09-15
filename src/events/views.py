from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from django.utils.timezone import get_current_timezone
import json
from datetime import datetime, timedelta

CALOPTIONS = """
    header: {
      left: 'prev,next title',
      center: '',
      right: 'month,agendaWeek,agendaDay today',
    },
    aspectRatio: 2,
    fixedWeekCount: true, // Always show months with 6 weeks, even if month has fewer
    businessHours: {
      start: '10:00',
      end: '18:00',
      dow: [1,2,3,4]
    },
    minTime: '08:00:00',
    maxTime: '23:00:00',
    allDaySlot: true,     // Show all-day events in their own section above the rest (if false, they aren't shown at all)
    //eventLimit: true,     // Show "more" link when too many events
    editable: true
"""

'''CALSOURCES = """
    googleCalendarApiKey: '<API Key>',
    eventSources: [
      {
        url: "/eventjson/",
        className: 'calitem_blue'
      },
      {
        googleCalendarId: 'csusb.infosec.club@gmail.com',
        className: 'gcinfosec'
      }
    ]
"""'''

CALSOURCES = """
    events: {
        url: "/eventjson/",
        className: 'calitem_blue'
    }
"""

CALHOOKS = """
    dayClick: function() {
      alert('a day has been clicked!');
      $('#calendar').fullCalendar('next');
    }
"""

def calendar(request):
  context = {
    'calendar_config_options': CALOPTIONS + "," + CALSOURCES + "," + CALHOOKS
  }
  return render(request, 'infosec/calendar.html', context)

def eventjson(request):
  margin = timedelta(days=1)
  start = datetime.strptime(request.GET["start"], "%Y-%m-%d") - margin
  end = datetime.strptime(request.GET["end"], "%Y-%m-%d") + margin
  events = Event.objects.filter(end__gte=start).filter(start__lte=end)
  events_values = list(events.values('id', 'title', 'start', 'end', 'allDay'))
  jsondump = json.dumps(events_values,
      default=lambda obj: obj.astimezone(get_current_timezone()).isoformat() if hasattr(obj, 'isoformat') else obj)
  return HttpResponse(jsondump, content_type='application/json')
