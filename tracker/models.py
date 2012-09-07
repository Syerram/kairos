from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from kairos.util.monkey_patch import decorator as monkey_patch
from categories.models import Project, Activity
from common.models import DropdownValue

class Timesheet(models.Model):
    """
        Represents timesheet per week per project per day
    """
    
    project = models.ForeignKey(Project)
    activity = models.ForeignKey(Activity)
    day = models.DateTimeField(auto_now_add=True)
    
    day_1_hours = models.DecimalField(_('day one hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_2_hours = models.DecimalField(_('day two hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_3_hours = models.DecimalField(_('day three hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_4_hours = models.DecimalField(_('day four hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_5_hours = models.DecimalField(_('day five hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_6_hours = models.DecimalField(_('day six hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    day_7_hours = models.DecimalField(_('day seven hours'), max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    
    def __total_hours(self):
        """Determines the amount of total hours for the time period"""
        return (self.day_1_hours or 0) + (self.day_2_hours or 0) + (self.day_3_hours or 0) + \
            (self.day_4_hours or 0) + (self.day_5_hours or 0) + (self.day_6_hours or 0) + (self.day_7_hours or 0)
    
    total_hours = property(__total_hours)
    
    def __notes(self):
        return TimesheetNote.objects.get(timesheet=self)
    
    notes = property(__notes)
    
class TimesheetNote(models.Model):
    """
        Represents notes for each time sheet. 
    """
    timesheet = models.ForeignKey(Timesheet)
    
    day_1_note = models.CharField(max_length=1000, null=True, blank=True)
    day_2_note = models.CharField(max_length=1000, null=True, blank=True)
    day_3_note = models.CharField(max_length=1000, null=True, blank=True)
    day_4_note = models.CharField(max_length=1000, null=True, blank=True)
    day_5_note = models.CharField(max_length=1000, null=True, blank=True)
    day_6_note = models.CharField(max_length=1000, null=True, blank=True)
    day_7_note = models.CharField(max_length=1000, null=True, blank=True)

class WeekSnapshotManager(models.Manager):
        
    def in_period(self, week, user):
        #the dates passed in have time element, so we are using min/max time to get all timesheets
        week_snapshot_mgr = self.get_query_set().filter(week=week, user=user).prefetch_related('timesheets')
        if week_snapshot_mgr.exists():
            weeksnapshot = week_snapshot_mgr.all()[0]
            timesheets = weeksnapshot.timesheets.all()
            return weeksnapshot, timesheets
        return None, self.get_query_set().none()
    
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except WeekSnapshot.DoesNotExist:
            return None

class WeekSnapshot(models.Model):
    """holds the week snapshot of timesheets"""
    
    start_week = models.DateTimeField()
    end_week = models.DateTimeField()
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    week = models.PositiveIntegerField(_('week number'))    
    
    user = models.ForeignKey(User)
    
    timesheets = models.ManyToManyField(Timesheet, null=True, blank=True)
    
    def __history(self):
        return WeekSnapshotHistory.objects.get(weeksnapshot=self)
    
    history = property(__history)
    
    def __total_hours(self):
        """Returns total hours for all timesheets"""
        total_hours = 0
        for timesheet in self.timesheets.all():
            total_hours += timesheet.total_hours
        
        return total_hours
    
    total_hours = property(__total_hours)
    
    objects = WeekSnapshotManager()   


class WeekSnapshotHistory(models.Model):
    """Represents different statuses for weekly timesheets"""
    weeksnapshot = models.ForeignKey(WeekSnapshot)
    weeksnapshot_status = models.ForeignKey(DropdownValue)
    last_updated = models.DateTimeField(auto_now=True)   

    def __unicode__(self):
        return self.weeksnapshot_status.name

@monkey_patch(WeekSnapshot)
class PatchedWeekSnapshot(object):
    
    def __last_status(self):
        """If it doesn't exists, returns by default DRAFT status"""
        #TODO create settings attribute instead of hardcoding to DRAFT    
        try:
            return WeekSnapshotHistory.objects.filter(Q(weeksnapshot=self)).latest(field_name='last_updated')
        except WeekSnapshotHistory.DoesNotExist:
            draft_dropdownvalue = DropdownValue.objects.dropdownvalue('WF', 'DRAFT')
            return WeekSnapshotHistory(weeksnapshot=self, weeksnapshot_status=draft_dropdownvalue)
    
    last_status = property(__last_status)   
    
    def __last_workflow(self):
        """return brand new workflow object or existing workflow instance"""
        return None
        
