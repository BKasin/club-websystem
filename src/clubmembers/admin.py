from django.contrib import admin

# Register your models here.
from .models import Club, Member, Membership
admin.site.register(Club)
admin.site.register(Member)
admin.site.register(Membership)
