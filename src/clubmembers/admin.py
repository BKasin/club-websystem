from django.contrib import admin

# Register your models here.
from .models import Club, Member, Membership

class ClubAdmin(admin.ModelAdmin):
  class Meta:
    model = Club
class MemberAdmin(admin.ModelAdmin):
  class Meta:
    model = Member
class MembershipAdmin(admin.ModelAdmin):
  class Meta:
    model = Membership

admin.site.register(Club, ClubAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Membership, MembershipAdmin)
