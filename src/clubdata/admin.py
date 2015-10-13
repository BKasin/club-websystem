from django.contrib import admin

from .models import Club


class ClubAdmin(admin.ModelAdmin):
  list_display = ('name_short', 'name_long', 'site')


admin.site.register(Club, ClubAdmin)
