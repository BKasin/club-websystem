import json
from datetime import date, datetime, timedelta

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.contrib import messages

from .models import Event, RecurringEvent
from .forms import EventEditForm, duration_string



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






NORECURRING = 0
rule_type_onetime = (
  (NORECURRING, 'One-time'),
)

def event_manage(request, eventid=None, editrecurring=False):
  if not request.user.has_perm('events.add_event'):
    raise Http404("You do not have privileges to create events.")

  context = {}

  if request.method == 'POST':
    # User posted changes
    form = EventEditForm(request.POST)
    form.fields['rule_type'].choices = rule_type_onetime + RecurringEvent.rule_type_choices
    if form.is_valid():
      rt = form.cleaned_data['rule_type']
      context['rule_type_int'] = rt
      if rt == NORECURRING:
        # It's a regular event, so we can just create it and move on
        all_day = form.cleaned_data['all_day']
        if all_day:
          start = form.cleaned_data['start_date']
        else:
          start = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
        e = Event(
          club=None,
          title = form.cleaned_data['title'],
          start = start,
          duration = form.cleaned_data['duration'],
          all_day = all_day,
        )
        e.save()
        return render(request, "events_submitandrefresh.html")

      else:
        # It's a recurring event
        re = RecurringEvent(
          starts_on = form.cleaned_data['start_date'],
          ends_on = form.cleaned_data['end_date'],
          rule_type = rt,
          repeat_each = form.cleaned_data['repeat_each'],
          criteria = form.cleaned_data['criteria'],
        )
        dates = re.dates_per_rule_iter()
        all_day = form.cleaned_data['all_day']
        if not all_day: time = form.cleaned_data['start_time']
        duration = form.cleaned_data['duration']

        if '_submitpreview' in request.POST:
          # User wants a preview of the events to be created
          context['events'] = dates
          if all_day:
            context['events_time'] = "All day"
          else:
            context['events_time'] = time.strftime('%-I:%M %p')
          context['events_duration'] = duration_string(duration)
          context['show_events_preview'] = True

        else:
          # User wants to actually create the events
          try:
            with transaction.atomic():
              # Save the recurring event group, so we can get its ID
              re.save()

              # Create the individual events
              title = form.cleaned_data['title']
              club = None
              for d in dates:
                if all_day:
                  start = d
                else:
                  start = datetime.combine(d, time)
                e = Event(
                  club=club,
                  title = title,
                  start = start,
                  duration = duration,
                  all_day = all_day,
                  recurring = re,
                )
                e.save()
              return render(request, "events_submitandrefresh.html")

          except:
            # By this point, Django has already rolled back the transaction
            messages.error(request, "An error occured while attempting to create the events.")

    else:
      # Even if the form failed validation, we still need this...
      context['rule_type_int'] = form.cleaned_data['rule_type']

    # If we got to this point, then there must have been form errors, so show the form
    context['add'] = True

  else:
    if eventid:
      if not editrecurring:
        # Initial load of the form (editing an existing regular event)
        e = Event.objects.get(id=eventid)
        context['eventid'] = eventid
        if e.recurring:
          context['linked_recurringevent'] = e.recurring
        rt = NORECURRING
        context['rule_type_int'] = rt
        initialdata = {
          'title': e.title,
          'rule_type': rt,
          'start_date': e.start.date(),
          'start_time': e.start.time(),
          'duration': e.duration,
          'all_day': e.all_day,
        }
        form = EventEditForm(initial=initialdata)
        form.fields['rule_type'].choices = rule_type_onetime

      else:
        # Initial load of the form (editing an existing recurring event)
        return HttpResponse('not implemented yet')

    else:
      # Initial load of the form (creating a new event)
      rt = int(request.GET.get('rt', NORECURRING))
      context['rule_type_int'] = rt
      now = timezone.now()
      now_date = now.date()
      initialdata = {
        'rule_type': rt,
        'start_date': now_date,
        'end_date': now_date,
        'repeat_each': 1,
        'start_time': round_time(now, 60*60).time(),   # Round the current time to the nearest hour
        'duration': timedelta(hours=get_default_event_hours()),
        'all_day': False,
      }
      initial_start = request.GET.get('start', None)
      if initial_start:
        try:
          d = datetime.strptime(initial_start, "%Y-%m-%dT%H:%M:%S")
          # If the above succeeded, then 'start' is a date/time
          initialdata['start_date'] = d.date()
          initialdata['start_time'] = d.time()
          initialdata['duration'] = timedelta(hours=get_default_event_hours())
        except ValueError:
          try:
            d = datetime.strptime(initial_start, "%Y-%m-%d")
            # If the above succeeded, then 'start' is only a date
            initialdata['start_date'] = d.date()
            initialdata['start_time'] = None
            initialdata['duration'] = timedelta(days=get_default_event_days())
            initialdata['all_day'] = True
          except ValueError:
            pass
      form = EventEditForm(initial=initialdata)
      form.fields['rule_type'].choices = rule_type_onetime + RecurringEvent.rule_type_choices
      context['add'] = True

  context['is_popup'] = True
  context['form'] = form
  return render(request, "events_edit.html", context)









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
    initial_data = {
      'rule_type': NORECURRING,
      'title': event.title,
      'start_date': event.start.date(),
      'start_time': event.start.time(),
      'duration': event.duration,
      'all_day': event.all_day,
    }
    form = EventEditForm(initial=initial_data)

  context = {
    'form': form,
    'add': False,
    'eventid': eventid,
    'initial_rule_type': NORECURRING,
    'is_popup': True
  }
  return render(request, "events_edit.html", context)

def event_editrecurring(request, eventid):
  if not request.user.has_perm('events.change_eventrecurring'):
    raise Http404("You do not have privileges to edit recurring events.")

  return HttpResponse('ok')





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
