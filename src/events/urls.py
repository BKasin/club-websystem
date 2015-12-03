from django.conf.urls import url

from views import calendarpage, jsonsearch, fcdragmodify, EventManager, event_view

event_manager = EventManager.as_view()
urlpatterns = [
  url(r'^$', calendarpage, name='events'),
  url(r'^json/', jsonsearch, name='jsonsearch'),
  url(r'^modify/', fcdragmodify, name='fcdragmodify'),

  url(r'^new/', event_manager, name='newevent'),
  url(r'^(?P<eventid>\d+)/edit/', event_manager, name='editevent'),
  url(r'^recurring/(?P<eventid>\d+)/edit/(?:orig-(?P<originaleventid>\d+)/)?', event_manager, {'editingregularevent': False}, name='editrecurringevent'),

  # Must be last...
  url(r'^(?P<eventid>\d+)/', event_view, name='viewevent'),
]
