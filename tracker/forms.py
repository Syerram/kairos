'''
Created on Aug 15, 2012

@author: staticfish
'''
from django.forms.models import ModelForm
from tracker.models import Timesheet, WeekSnapshot
from django import forms

class TimesheetForm(ModelForm):
    total_hours = forms.DecimalField(required=False)
    
    class Meta:
        model = Timesheet
        
    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['total_hours'] = instance.total_hours

class WeekSnapshotForm(ModelForm):
    total_hours = forms.DecimalField(required=False)
    
    class Meta:
        model = WeekSnapshot
        exclude = ('user', 'timesheets')

    def __init__(self, *args, **kwargs):
        super(WeekSnapshotForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['total_hours'] = instance.total_hours

    def save(self, user, commit=True):
        self.instance.user = user
        return ModelForm.save(self, commit=commit)
