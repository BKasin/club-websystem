from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^manage/$', views.membershipmanager, name='membershipmanager'),
]
