from django.contrib import admin

# Register your models here.
from .models import Content

class ContentAdmin(admin.ModelAdmin):
  class Meta:
    model = Content

admin.site.register(Content, ContentAdmin)
