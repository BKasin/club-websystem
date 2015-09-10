from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Our site
    url(r'^$', 'mainsite.views.home', name='home'),
    url(r'^about/$', 'mainsite.views.about', name='about'),
    url(r'^pagemd/(?P<page>\w+)/$', 'contentblocks.views.pagemd', name='pagemd'),

    # Built-in pages
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
