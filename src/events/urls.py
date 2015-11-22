from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.events, name='events'),
  url(r'^json/', views.jsonsearch, name='jsonsearch'),
  url(r'^modify/', views.fcdragmodify, name='fcdragmodify'),

  url(r'^new/', views.event_new, name='newevent'),
  url(r'^(?P<eventid>.+)/edit/', views.event_edit, name='editevent'),

  url(r'^recurring/new/', views.event_newrecurring, name='newrecurringevent'),
  url(r'^recurring/(?P<eventid>.+)/edit/', views.event_editrecurring, name='editrecurringevent'),

  # Must be last...
  url(r'^(?P<eventid>.+)/', views.event_view, name='viewevent'),
]
