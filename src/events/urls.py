from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.events, name='events'),
  url(r'^json/', views.eventjson, name='eventjson'),
  url(r'^modify/', views.eventmodify, name='eventmodify'),
]
