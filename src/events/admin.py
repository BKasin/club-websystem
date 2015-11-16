from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
  list_display = ('title', 'start', 'duration', 'all_day')
  ordering = ('start',)


admin.site.register(Event, EventAdmin)
