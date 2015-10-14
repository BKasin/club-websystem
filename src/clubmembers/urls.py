from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^profile/$', views.userprofile, name='userprofile'),
  url(r'^profile/confirmemail/(?P<confirmation_key>\w+)/', views.confirmemail, name='confirmemail'),
]
