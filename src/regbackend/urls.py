from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import TemplateView

from .views import RegistrationView
from .forms import RegistrationFormWithoutEmail

urlpatterns = patterns('',
  url(r'^register/closed/$',
    TemplateView.as_view(template_name='registration/registration_closed.html'),
    name='registration_disallowed'),
  url(r'^register/complete/$',
    TemplateView.as_view(template_name='registration/registration_complete.html'),
    name='registration_complete'),
)

if getattr(settings, 'INCLUDE_REGISTER_URL', True):
  urlpatterns += patterns('',
    url(r'^register/$',
      RegistrationView.as_view(form_class=RegistrationFormWithoutEmail),
      name='registration_register'
    ),
  )

if getattr(settings, 'INCLUDE_AUTH_URLS', True):
  urlpatterns += patterns('',
    (r'', include('registration.auth_urls')),
  )
