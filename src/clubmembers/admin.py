from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member, Membership, PendingEmailChange





class MemberAdmin(UserAdmin):
  # Custom admin class for our Member model

  # Fields to show when editing a user
  fieldsets = (
    ('Authentication', {'fields': ('username', 'password', 'pin_hash', 'last_login',)}),
    ('Personal', {'fields': ('name_first', 'name_last', 'coyote_id',)}),
    ('Contact', {'fields': ('email', 'email_pending', 'phone', 'texting_ok',)}),
    ('Photo', {'fields': ('photo',)}),
    ('Academic', {'fields': ('acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',)}),
    ('Other', {'fields': ('shirt_size',)}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
  )

  # Fields that should use a split selected & unselected interface, instead of the default Ctrl+Click to multi-select
  filter_horizontal = ('groups', 'user_permissions',)

  # Fields to ask for when creating a new user
  add_form_template = 'admin/add_member_form.html'
  add_fieldsets = ((None, {
    'classes': ('wide',),
    'fields': ('username', 'password1', 'password2', 'name_first', 'name_last', 'coyote_id', 'email', 'is_active')
  }),)

  # Fields that show on the admin page as columns
  list_display = ('username', 'name_first', 'name_last', 'coyote_id', 'email', 'phone', 'is_active', 'is_staff')

  # Filters available along the right side
  list_filter = (
    'groups',
    'is_active', 'is_staff',
    'acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',
  )

  # Fields to search through when admin performs a text search on the member list
  search_fields = ('username', 'name_first', 'name_last', 'coyote_id', 'email', 'phone')

  # Default sort order of the list
  ordering = ('name_last', 'name_first',)












class MembershipAdmin(admin.ModelAdmin):
  list_display = ('member', 'club')
  raw_id_fields = ['member']












class PendingEmailChangeAdmin(admin.ModelAdmin):
  actions = ['confirm_emails']
  list_display = ('member', 'pendingchange_tostr', 'confirmation_key_expired')
  search_fields = ('member__username', 'member__email', 'member__emailpending')
  raw_id_fields = ['member']

  def pendingchange_tostr(self, obj):
    return '%s --> %s' % (obj.member.email, obj.member.email_pending)
  pendingchange_tostr.short_description = "Pending change"

  def confirm_emails(self, request, queryset):
    for c in queryset:
      PendingEmailChange.objects.confirm_pendingemail(c.confirmation_key)
  confirm_emails.short_description = "Confirm/apply email changes"





admin.site.register(Member, MemberAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(PendingEmailChange, PendingEmailChangeAdmin)
