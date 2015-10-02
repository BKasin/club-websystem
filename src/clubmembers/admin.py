from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.forms import AdminAuthenticationForm

from .models import Member, Membership

class CustomAdminLoginForm(AdminAuthenticationForm):
  # Extend Django's default admin login form, simply to change the label
  # on the username field
  error_messages = {
    'invalid_login': "Please enter the correct credentials of a user with admin privileges. Note that both fields are case-sensitive.",
  }
  username = forms.CharField(label='Username / email / coyote id', max_length=254)

class MemberAdmin(UserAdmin):
  # Custom admin class for our Member model

  # Fields to show when editing a user
  fieldsets = (
    ('Authentication', {'fields': ('username', 'password')}),
    ('Personal', {'fields': ('name_first', 'name_last', 'coyote_id',)}),
    ('Contact', {'fields': ('email', 'phone', 'texting_ok',)}),
    #('Photo', {'fields': ('photo',)}),
    ('Academic', {'fields': ('acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',)}),
    ('Other', {'fields': ('shirt_size',)}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
  )

  # Fields that should use a split selected & unselected interface, instead of the default Ctrl+Click to multi-select
  filter_horizontal = ('groups', 'user_permissions',)

  # Fields to ask for when creating a new user
  add_form_template = 'admin_add_member_form.html'
  add_fieldsets = (
    (None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2', 'coyote_id', 'name_first', 'name_last', 'email',)}),
  )

  # Fields that show on the admin page as columns
  list_display = ('name_first', 'name_last', 'coyote_id', 'email', 'is_staff', 'is_superuser')

  # Filters available along the right side
  list_filter = (
    'groups',
    'is_active', 'is_staff',
    'acad_major', 'acad_minor', 'acad_concentration', 'acad_grad_qtr',
  )

  # Fields to search through when admin performs a text search on the member list
  search_fields = ('username', 'name_first', 'name_last', 'coyote_id', 'email')

  # Default sort order of the list
  ordering = ('name_last', 'name_first',)



admin.site.login_form = CustomAdminLoginForm
admin.site.register(Member, MemberAdmin)
admin.site.register(Membership)
