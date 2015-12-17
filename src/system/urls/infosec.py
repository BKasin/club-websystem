from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from mainsite_infosec.views import home, events_preview, about_contact
from contentblocks.views import contentblock_view, contentblock_edit

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

urlpatterns = [
  # Main site
  url(r'^$', home, {'event_preview_days': 14}, name='home'),
  url(r'^events_preview/$', events_preview, {'event_preview_days': 14}, name='eventspreview'),
  url(r'^about_contact/$', about_contact, name='about_contact'),

  # URLConfs from apps
  url(r'^events/', include('events.urls')),
  url(r'^member/', include('clubmembers.urls')),

  # django-wiki
  url(r'^notifications/', get_nyt_pattern()),
  url(r'^wiki/', get_wiki_pattern()),

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
