from django.db import models
from categories.models import Project, Activity
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _

from kairos import util
from common.models import DropdownModel

class TimesheetManager(models.Manager):
    
    def current(self, user=None):
        return self._in_period(util.determine_period(), user)
    
    def notes(self, timesheet):
        return TimesheetNote.objects.get(timesheet=timesheet)
    
    def _in_period(self, week, user):
        return self.get_query_set().filter(start_week__lte=week[0], end_week__gte=week[1], user=user)


# Create your models here.
class Timesheet(models.Model):
    """
        Represents timesheet per week per project per day
    """
    
    project = models.ForeignKey(Project)
    activity = models.ForeignKey(Activity)
    day = models.DateTimeField(auto_now_add=True)
    
    day_1_hours = models.DecimalField(_('day one hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_2_hours = models.DecimalField(_('day two hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_3_hours = models.DecimalField(_('day three hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_4_hours = models.DecimalField(_('day four hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_5_hours = models.DecimalField(_('day five hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_6_hours = models.DecimalField(_('day six hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    day_7_hours = models.DecimalField(_('day seven hours'), max_digits=4, decimal_places=2, null=True, blank=True)
    
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    
    objects = TimesheetManager()
    
    def __total_hours(self):
        """Determines the amount of total hours for the time period"""
        return self.day_1_hours + self.day_2_hours + self.day_3_hours + self.day_4_hours + self.day_5_hours + self.day_6_hours + self.day_7_hours
    
    total_hours = property(__total_hours)
    
    def __available_statuses(self):
        return DropdownModel.objects.get(category='TS')
    
    available_statuses = property(__available_statuses)
        

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

class TimesheetHistory(models.Model):
    """Represents different statuses for timesheet"""
    timesheet = models.ForeignKey(Timesheet)
    timesheet_status = models.ForeignKey(DropdownModel)
    last_updated = models.DateTimeField(auto_now=True)   

class WeekSnapshot(models.Model):
    """holds the week snapshot of timesheets"""
    
    start_week = models.DateTimeField()
    end_week = models.DateTimeField()
    
    user = models.ForeignKey(User)
    
    timesheets = models.ManyToManyField(Timesheet, null=True, blank=True)
