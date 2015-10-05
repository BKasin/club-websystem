from django.db import models

# Create your models here.
class MeetingType(models.Model):
    #id
    title = models.CharField(max_length=150, blank=False, null=False)

    def __unicode__(self): #__str__ in python 3
        return self.title

class Meeting(models.Model):
    #id
    title = models.CharField(max_length=150, blank=False, null=False)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    meeting_type = models.ForeignKey(MeetingType, related_name='meetings')
    club_id = models.ForeignKey(clubdata.Club, related_name='meetings')
    active = models.BooleanField(null=False)
    first_created = models.DateTimeField(auto_now=True, auto_now_add=False, null=False)
    last_edited = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __unicode__(self): #__str__ in python 3
        return self.title

class ScanType(models.Model):
    #id
    title = models.CharField(max_length=150, blank=False, null=False)

    def __unicode__(self): #__str__ in python 3
        return self.title

class AttendanceLog(models.Model):
    #id
    coyote_id = models.ForeignKey(clubmembers.Member, to_field='coyote_id', related_name='attendance', null=True)
    scan_type = models.ForeignKey(ScanType, related_name='+')
    guest = models.BooleanField(null=False)
    meeting_id = models.ForeignKey(Meeting, related_name='attendees')
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False, null=False)

    class Meta:
        verbose_name = "Attendance Log"
        verbose_name_plural = "Attendance Log"

    def __unicode__(self): #__str__ in python 3
        return self.coyote_id
