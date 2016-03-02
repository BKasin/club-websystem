from datetime import timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import ContactForm

from utils.templateemail import send_template_email
from clubmembers.models import Member
from events.models import Event

def _get_preview_of_events(event_preview_days):
  if not event_preview_days: event_preview_days=7
  now = timezone.now()
  range_start = now - timedelta(days=1)
  range_end = now + timedelta(days=event_preview_days)
  return Event.objects.filter(start__gte=range_start, start__lte=range_end)

def home(request, event_preview_days=None):
  context = {
    'events': _get_preview_of_events(event_preview_days),
    'event_preview_days': event_preview_days,
  }
  return render(request, "home.html", context)

def events_preview(request, event_preview_days=None):
  context = {
    'events': _get_preview_of_events(event_preview_days),
    'event_preview_days': event_preview_days,
    'is_popup': True,
  }
  return render(request, "home_eventpreview1.html", context)

def about_contact(request):
  if request.user.is_anonymous():
    initial=None
  else:
    initial = {'full_name':request.user.get_full_name(), 'email':request.user.email}
  form = ContactForm(request.POST or None, initial=initial)

  if form.is_valid():
    senderemail = form.cleaned_data['email']
    send_template_email(request,
      template_prefix='contact_email',
      to=settings.GENERIC_CONTACT_EMAIL,
      reply_to=[senderemail],
      extra_context={
        'sendername': form.cleaned_data['full_name'],
        'senderemail': senderemail,
        'message': form.cleaned_data['message'],
      }
    )

    messages.success(request, "Your email has been sent successfully.")
    return redirect(about_contact)

  context = {
    "form": form,
  }
  return render(request, "about_contact.html", context)
