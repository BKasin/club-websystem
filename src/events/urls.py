from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.events, name='events'),
  url(r'^json/', views.jsonsearch, name='jsonsearch'),
  url(r'^modify/', views.fcdragmodify, name='fcdragmodify'),

  url(r'^new/', views.event_manage, name='newevent'),
  url(r'^(?P<eventid>\d+)/edit/', views.event_manage, name='editevent'),
  url(r'^recurring/(?P<eventid>\d+)/edit/', views.event_manage, {'editrecurring': True}, name='editrecurringevent'),

  # Must be last...
  url(r'^(?P<eventid>\d+)/', views.event_view, name='viewevent'),
]
