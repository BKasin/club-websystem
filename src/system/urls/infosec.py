from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from mainsite_infosec.views import home, about_contact
from contentblocks.views import contentblock_view, contentblock_edit

urlpatterns = [
  # Main site
  url(r'^$', home, name='home'),
  url(r'^about_contact/$', about_contact, name='about_contact'),

  # URLConfs from apps
  url(r'^events/', include('events.urls')),
  url(r'^member/', include('clubmembers.urls')),

  # Django apps
  url(r'^admin/', include(admin.site.urls)),
  url(r'^accounts/', include('regbackend.urls')),

  # Contentblock processor (must be last)
  url(r'^(?P<page>\w+)/$', contentblock_view, name='contentblock_view'),
  url(r'^(?P<page>\w+)/edit/$', contentblock_edit, name='contentblock_edit'),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
