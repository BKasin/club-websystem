import json
from datetime import date, time, datetime, timedelta

from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.views.generic import View

from .models import Event, RecurringEvent
from .forms import EventEditForm, duration_string



# Helper functions
event_manager_perms = (
  'events.add_event',
  'events.change_event',
  'events.delete_event',
  'events.add_recurringevent',
  'events.change_recurringevent',
  'events.delete_recurringevent',
)
error_insufficient_perms = Http404("You do not have privileges to manage events.")

def round_time(dt, roundTo):
  """
  Round a datetime object to any time lapse in seconds
  dt = datetime.datetime object
  roundTo = Closest number of seconds to round to
  """
  seconds = (dt - dt.min).seconds
  rounding = (seconds+roundTo/2) // roundTo * roundTo
  return dt + timedelta(0,rounding-seconds,-dt.microsecond)

def get_default_event_hours():
  """
  Looks up the default duration of timed events. If this hasn't been overridden in settings,
  use 2 hours long as the default.
  """
  return getattr(settings, 'EVENTS_DEFAULT_HOURS', 2)

def get_default_event_days():
  """
  Looks up the default duration of all-day events. If this hasn't been overridden in settings,
  use 1 day long as the default.
  """
  return getattr(settings, 'EVENTS_DEFAULT_DAYS', 1)








####################################################################################################
# Event calendar and event feed
####################################################################################################

def jsonsearch(request):
  """
  This is our calendar feed, used by FullCalendar.
  """

  # This is an efficient, but not correct, way of finding events within the desired range. A more
  #   correct way would be to query the database as .filter(end__gte=start, start__lte=end)
  #   But we can't do this because we don't store the end time in the database, only a duration.
  #   Rather than have SQL compute the end time as start+duration, we just use a margin factor to
  #   collect a few extra days on each end. FullCalendar will filter out the extra events.
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
  """
  When the user drags and drops or resizes an event in FullCalendar, we can do some simple modify
  operations here without using the full edit form
  """
  if not request.user.has_perms(event_manager_perms): raise error_insufficient_perms

  # Lookup the event
  e = Event.objects.get(id=int(request.GET["id"]))
  newallday = True if (request.GET["allday"]=='true') else False
  newstart = datetime.utcfromtimestamp(float(request.GET["newstart"]))
  newend = request.GET["newend"]

  # Modify the event
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

def calendarpage(request):
  """
  Renders the calendar page
  """
  has_perms = request.user.has_perms(event_manager_perms)
  context = {
    'addperm': has_perms,
    'changeperm': has_perms,
    'defaulthours': get_default_event_hours(),
    'defaultdays': get_default_event_days(),
  }
  return render(request, "events.html", context)








####################################################################################################
# Event viewing and RSVPs
####################################################################################################

def event_view(request, eventid):
  event = Event.objects.get(id=eventid)
  context = {
    'event': event
  }
  return render(request, "events_view.html", context)








####################################################################################################
# Event management (creating, editing, deleting)
####################################################################################################

class EventManager(View):
  """
  Shows a full-featured form for creating, editing, or deleting events and recurring events.
  For both the 'get' and 'post' functions, the following apply:
    * If 'eventid' is None, the form will be used to create a new event (or recurring event). If
      'eventid' is an ID, then the form will be used to edit an existing event.
    * If 'editingregularevent' is True, then this request came from the /<id>/edit/ URL. If False, it
      came from the /recurring/<id>/edit/ URL. If 'eventid' is None, then this parameter is irrelevant.
  Notes:
    * Throughout this view, the 'initial_event_type' context variable is used to indicate the initial
      position of the Event Type slider switch. If we're in edit mode ('eventid' is not None), it
      also changes how the form looks and what features are available (for example, a recurring event
      cannot be edited to become a regular event). A possible alternative to using 'initial_event_type'
      is for the templates to query {{ form.event_type.value }}. But that is dangerous as it is
      accessing the form's data before it has been cleaned; sometimes this returns a string, and
      sometimes an integer.
    * The 'addmode' context variable is added, since templates cannot test 'eventid is None'. In the
      rare case that 'eventid' == 0, the template still needs to know that 'eventid' was specified,
      so it will know we're in EDIT mode and not ADD mode.
    * To reduce confusion, throughout this module and the related form and templates, 'rule_type'
      refers to the Daily/Weekly/Monthly choise on a RecurringEvent model instance. Whereas,
      'event_type' refers to the broader selection of OneTime/Daily/Weekly/Monthly that occurs prior
      to the determination of Event vs. RecurringEvent.
  """
  NORECURRING = 0
  event_type_onetime = (
    (NORECURRING, 'One-time'),
  )
  form_class = EventEditForm
  template_main = "events_edit.html"
  template_confirmdelete = "events_confirmdelete.html"
  template_successandrefresh = "events_submitandrefresh.html"

  current_club_id = None
  current_club_shortname = None

  def __init__(self, **kwargs):
    super(EventManager, self).__init__(**kwargs)
    current_club = Site.objects.get_current().club
    self.current_club_id = current_club.id
    self.current_club_shortname = current_club.name_short

  def get(self, request, editingregularevent=True, eventid=None, originaleventid=None):
    if not request.user.has_perms(event_manager_perms): raise error_insufficient_perms

    context = {}
    if eventid is None:   # Initial form to create an Event or RecurringEvent
      event_type = int(request.GET.get('et', self.NORECURRING))
      context['initial_event_type'] = event_type

      # Default field data
      now = timezone.now()
      now_date = now.date()
      initialdata = {
        'event_type': event_type,
        'start_date': now_date,
        'end_date': now_date,
        'repeat_each': 1,
        'start_time': round_time(now, 60*60).time(),   # Round the current time to the nearest hour
        'duration': timedelta(hours=get_default_event_hours()),
      }

      # If a date or a date/time was given in the URI, attempt to process it
      initial_start = request.GET.get('start', None)
      if initial_start:
        try:
          d = datetime.strptime(initial_start, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
          # Failed to process, so let's try the date/time check next
          try:
            d = datetime.strptime(initial_start, "%Y-%m-%d").date()
          except ValueError:
            # Failed to process, so let the form just use the defaults from initialdata
            pass
          else:
            # If the above succeeded, then 'start' is only a date
            initialdata['start_time'] = None
            initialdata['start_date'] = d
            initialdata['end_date'] = d
            initialdata['duration'] = timedelta(days=get_default_event_days())
            initialdata['all_day'] = True
        else:
          # If the above succeeded, then 'start' is a date/time
          initialdata['start_time'] = d.time()
          d = d.date()
          initialdata['start_date'] = d
          initialdata['end_date'] = d
          initialdata['duration'] = timedelta(hours=get_default_event_hours())

      # Load the form
      form = EventEditForm(initial=initialdata, event_type_choices=self.event_type_onetime+RecurringEvent.rule_type_choices)


    else:     # User wants to edit something
      if editingregularevent:
        # Editing an existing regular event
        e = Event.objects.get(id=eventid)
        if e.recurring_id:
          # Since this event is part of a series, redirect to the edit page for the series instead,
          #   unless the user specifically insists on editing the individual event.
          if int(request.GET.get('noredir', 0)) == 1:
            context['linked_recurringevent_id'] = e.recurring_id
          else:
            return redirect('editrecurringevent', eventid=e.recurring_id, originaleventid=e.id)

        # Populate the form
        context['initial_event_type'] = self.NORECURRING
        initialdata = {
          'event_type': self.NORECURRING,
          'title': e.title,
          'club_global': (e.club_id is None),
          'start_date': e.start.date(),
          'start_time': e.start.time(),
          'duration': e.duration,
          'all_day': e.all_day,
        }
        form = EventEditForm(initial=initialdata, event_type_choices=self.event_type_onetime)

        # Since this is a regular event, there is no extra confirmation step
        context['has_previewed'] = True

      else:
        # Editing an existing recurring event
        if originaleventid is not None:
          context['original_event_id'] = originaleventid
        re = RecurringEvent.objects.get(id=eventid)
        context['initial_event_type'] = re.rule_type
        initialdata = {
          'event_type': re.rule_type,
          'start_date': re.starts_on,
          'end_date': re.ends_on,
          'repeat_each': re.repeat_each,
          'criteria': re.criteria,
        }

        # Find the earliest Event that is linked to this RecurringEvent
        e = re.event_set.order_by('start').first()
        if e:
          initialdata['title'] = e.title
          initialdata['club_global'] = (e.club_id is None)
          initialdata['start_time'] = e.start.time()
          initialdata['duration'] = e.duration
          initialdata['all_day'] = e.all_day

        form = EventEditForm(initial=initialdata, event_type_choices=RecurringEvent.rule_type_choices)

    context['eventid'] = eventid
    context['addmode'] = (eventid is None)
    context['is_popup'] = True
    context['form'] = form
    context['current_club_shortname'] = self.current_club_shortname
    return render(request, self.template_main, context)




  def post(self, request, editingregularevent=True, eventid=None, originaleventid=None):
    if not request.user.has_perms(event_manager_perms): raise error_insufficient_perms
    context = {}
    if '_submitdelete' in request.POST:   # User wants to delete the item
      if editingregularevent:
        Event.objects.get(id=eventid).delete()
      else:
        # Deleting a recurring event is a major step, so we require a confirmation from the user
        re = RecurringEvent.objects.get(id=eventid)
        events = re.event_set.all()
        if request.POST.get('delete_confirm') != 'true':
          context['recurringevent'] = re
          context['events'] = events
          context['eventid'] = eventid
          context['is_popup'] = True
          return render(request, self.template_confirmdelete, context)
        else:
          # The Event model is intentionally set to Cascade Set Null, so that if we delete a
          #   RecurringEvent with linked Events that belong to another club (events that won't show
          #   up in the Event.objects manager anyway), those events will remain instead of being deleted.
          events.delete()
          re.delete()
      return render(request, self.template_successandrefresh)

    # At this point, the request could be for an Event or RecurringEvent, but we won't know
    #   which type until we process the form. The following processing must happen regardless if
    #   the form passes validation or not.
    if eventid is None:
      # We're creating a new event, so we can determine the event type from the form
      form = EventEditForm(data=request.POST, event_type_choices=self.event_type_onetime+RecurringEvent.rule_type_choices)
      form_valid = form.is_valid()
      event_type = form.cleaned_data['event_type']
    elif editingregularevent:
      # We're editing an existing regular event
      form = EventEditForm(data=request.POST, event_type_choices=self.event_type_onetime)
      form_valid = form.is_valid()
      event_type = self.NORECURRING
    else:
      # We're editing an existing recurring event
      form = EventEditForm(data=request.POST, event_type_choices=RecurringEvent.rule_type_choices)
      form_valid = form.is_valid()
      event_type = form.cleaned_data['event_type']
    context['initial_event_type'] = event_type

    if form_valid:    # No validation errors on the form
      if event_type == self.NORECURRING:    # It's a regular event, so we can just create/update it and move on
        if eventid is None:
          e = Event()
        else:
          e = Event.objects.get(id=eventid)
        e.title = form.cleaned_data['title']
        if form.cleaned_data['club_global'] == True:
          e.club_id = None
        else:
          e.club_id = self.current_club_id
        e.all_day = form.cleaned_data['all_day']
        if e.all_day:
          tm = time(0, 0, 0)
        else:
          tm = form.cleaned_data['start_time']
        e.start = datetime.combine(form.cleaned_data['start_date'], tm)
        e.duration = form.cleaned_data['duration']
        e.save()
        return render(request, self.template_successandrefresh)

      else:   # It's a recurring event, so it requires some special stuff
        # Create/update the series
        if eventid is None:
          re = RecurringEvent()
        else:
          re = RecurringEvent.objects.get(id=eventid)
        re.rule_type = event_type
        re.starts_on = form.cleaned_data['start_date']
        re.ends_on = form.cleaned_data['end_date']
        re.repeat_each = form.cleaned_data['repeat_each']
        re.criteria = form.cleaned_data['criteria']

        # Calculate which days should have events based on the criteria
        dates = re.dates_per_rule_iter()

        # Determine what the individual event should look like
        title = form.cleaned_data['title']
        if form.cleaned_data['club_global'] == True:
          club_id = None
        else:
          club_id = self.current_club_id
        all_day = form.cleaned_data['all_day']
        if all_day:
          tm = time(0, 0, 0)
        else:
          tm = form.cleaned_data['start_time']
        duration = form.cleaned_data['duration']

        if '_submitpreview' in request.POST:  # User just wants a preview of the events to be created
          events = []
          duration_str = duration_string(duration)
          # Generate initial list of events to be created
          for d in dates:
            events.append({
              'id': None,
              'start': datetime.combine(d, tm),
              'duration': duration_str,
              'all_day': all_day,
              'action': 'Will be added',
              'class': 'preview-add',
            })
          if eventid:
            # User is editing an existing recurring event, which likely has events already on the
            #   calendar, so we must calculate the changes to be made
            for e in re.event_set.all():
              found = False
              # For each event that actually exists already...
              if e.all_day==all_day:                # Initial filtering, since this does't require iterating through 'events'
                for eventdict in events:
                  if e.start==eventdict['start']:   # Further filtering
                    # This one matches an event we were about to add (at least with start_date,
                    #   start_time, and all_day), so look for non-critical data that must be updated
                    data_to_update = []
                    if e.title!=title: data_to_update.append('title')
                    if e.duration!=duration: data_to_update.append('duration')
                    if e.club_id!=club_id: data_to_update.append('club')
                    if len(data_to_update) == 0:
                      eventdict['action'] = 'Unchanged'
                      eventdict['class'] = 'preview-unchanged'
                    else:
                      eventdict['action'] = 'Update ' + ", ".join(data_to_update)
                      eventdict['class'] = 'preview-updatedata'
                    eventdict['id'] = e.id
                    found = True
                    break
              if not found:
                # This one doesn't match anything in our list, so it must be removed
                events.append({
                  'id': e.id,
                  'start': e.start,
                  'duration': duration_string(e.duration),
                  'all_day': e.all_day,
                  'action': 'Will be removed',
                  'class': 'preview-remove',
                })
            # Because we may have added new events to the list, out of order, we must sort the list
            events.sort(key=lambda x: x['start'])

          context['events'] = events
          context['show_events_preview'] = True

        else:   #No '_submitpreview', so user wants to actually create the events
          try:
            with transaction.atomic():
              # We have to save the recurring event group before we do anything else. Especially so,
              #   if this is a new one, since that is the only way we will get its ID.
              re.save()
              # Now do the hard part... process the individual events
              if not eventid:
                # We're creating a new recurring event, so simply create every individual event without analysis
                for d in dates:
                  e = Event(title=title, club_id=club_id, start=datetime.combine(d, tm), duration=duration, all_day=all_day, recurring=re)
                  e.save()
              else:
                # We're editing an existing recurring event, so we must make the minimum number of changes
                dates = map(lambda d: datetime.combine(d, tm), dates)
                events_to_delete = []
                for e in re.event_set.all():
                  found = False
                  # For each event that actually exists already...
                  if e.all_day==all_day:
                    for d in dates:
                      if e.start==d:
                        # This one matches an event we were about to add (at least with start_date,
                        #   start_time, and all_day), so update the other non-critical data
                        print(1)
                        e.title = title
                        e.club_id = club_id
                        e.duration = duration
                        print(2)
                        e.save()
                        print(3)

                        # Remove the date/time from the list, so we don't create a new event here below
                        dates.remove(d)
                        found = True
                        break
                  if not found:
                    # Mark this event for deletion. Don't delete it now, since that would be very slow.
                    events_to_delete.append(e.id)
                # Delete the events we previously marked for deletion
                Event.objects.filter(id__in=events_to_delete).delete()
                # Create the new events last
                for d in dates:
                  e = Event(title=title, club_id=club_id, start=d, duration=duration, all_day=all_day, recurring=re)
                  e.save()

              return render(request, self.template_successandrefresh)
          except:
            # By this point, Django has already rolled back the transaction
            messages.error(request, "An error occured while attempting to create the events.")

    # If we got to this point, then there must have been form errors or the user asked for a preview
    context['eventid'] = eventid
    context['addmode'] = (eventid is None)
    context['is_popup'] = True
    context['form'] = form
    context['current_club_shortname'] = self.current_club_shortname
    return render(request, self.template_main, context)
