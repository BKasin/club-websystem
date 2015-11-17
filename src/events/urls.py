from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.events, name='events'),
  url(r'^json/', views.jsonsearch, name='jsonsearch'),
  url(r'^modify/', views.fcdragmodify, name='fcdragmodify'),

  url(r'^new/', views.event_new, name='newevent'),
  url(r'^(?P<eventid>.+)/edit/', views.event_edit, name='editevent'),

  # Must be last...
  url(r'^(?P<eventid>.+)/', views.event_view, name='viewevent'),
]
