from django.contrib import admin

# Register your models here.
from .models import Block

class BlockAdmin(admin.ModelAdmin):
  # Fields to show when editing a user
  fieldsets = (
    ('Identification', {'fields': ('uniquetitle', 'description',)}),
    ('Publishing', {'fields': ('site', 'published',)}),
    ('Content', {'fields': ('datatype', 'blob',)}),
    ('Tracking', {'fields': ('created_date', 'created_by_user', 'edited_date', 'edited_by_user',)}),
  )

  # Fields that show on the admin page as columns
  list_display = ('uniquetitle', 'description', 'datatype', 'site', 'published')

  # Filters available along the right side
  list_filter = ('datatype', 'site', 'published', 'created_by_user', 'edited_by_user')

  # Fields to search through when admin performs a text search on the member list
  search_fields = ('uniquetitle', 'description', 'blob')

  # Default sort order of the list
  ordering = ('site', 'uniquetitle')

admin.site.register(Block, BlockAdmin)
