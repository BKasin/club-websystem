import json
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import Event
from .forms import EventEditForm

def events(request):
  context = {
    'addperm': request.user.has_perm('events.add_event'),
    'changeperm': request.user.has_perm('events.change_event'),
  }
  return render(request, "events.html", context)

def event_view(request, eventid):
  return HttpResponse('(to be implemented)')

def event_edit(request, eventid):
  if not request.user.has_perm('events.change_event'):
    raise Http404("You do not have privileges to edit events.")

  if not request.method == 'POST':
    # Initial load of the form
    event = Event.objects.get(id=eventid)
    form = EventEditForm(instance=event)

  else:
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

  context = {
    'form': form,
    'add': False,
    'eventid': eventid,
    'is_popup': True
  }
  return render(request, "events_editform.html", context)

def event_new(request):
  if not request.user.has_perm('events.add_event'):
    raise Http404("You do not have privileges to create events.")

  if not request.method == 'POST':
    # Initial load of the form
    initialstart = request.GET.get('start', None)
    if initialstart:
      try:
        initialstart = datetime.strptime(initialstart, "%Y-%m-%dT%H:%M:%S")
        form = EventEditForm(initial={'start': initialstart})
      except ValueError:
        try:
          initialstart = datetime.strptime(initialstart, "%Y-%m-%d")
          form = EventEditForm(initial={'start': initialstart, 'all_day': True})
        except ValueError:
          form = EventEditForm()
    else:
      form = EventEditForm()

  else:
    # User posted changes
    form = EventEditForm(request.POST)

    if form.is_valid():
      form.instance.save()
      context = {
        'form': form,
      }
      return render(request, "events_submitandrefresh.html", context)

  context = {
    'form': form,
    'add': True,
    'is_popup': True
  }
  return render(request, "events_editform.html", context)

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

def fcdragmodify(request):
  if not request.user.has_perm('events.change_event'):
    raise Http404("You do not have privileges to edit events.")

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
