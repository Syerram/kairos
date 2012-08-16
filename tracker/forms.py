'''
Created on Aug 15, 2012

@author: staticfish
'''
from django.forms.models import ModelForm
from tracker.models import Timesheet, WeekSnapshot

class TimesheetForm(ModelForm):
    
    class Meta:
        model = Timesheet
        
class WeekSnapshotForm(ModelForm):
    
    class Meta:
        model = WeekSnapshot
        exclude = ('user', 'timesheets')