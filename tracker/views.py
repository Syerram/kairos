# Create your views here.
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from kairos.util import determine_period, render_to_html_dict
from tracker.forms import TimesheetForm, WeekSnapshotForm
from tracker.models import WeekSnapshot

@login_required
@render_to_html_dict(
                     {'timesheet':'timetracker/timesheet.html',
                      'home-r': 'home.html'
                    })
def current_timesheet(request):
    """
    Current timesheet pulls the current week from the database. 
    if one doesn't exists, it creates in-mem object.
    If Post, saves it to the database
    """
    if request.method == 'GET':
        user_projects = request.user.get_profile().projects
        start_week, end_week = determine_period()    
        
        #prepare formset
        #TODO pull existing if present
        timesheet_form_set = formset_factory(TimesheetForm)
        week_snapshot = WeekSnapshot(start_week=start_week, end_week=end_week, user=request.user) 
        week_snapshot_form = WeekSnapshotForm(instance=week_snapshot)
        
        return 'timesheet', {'projects': user_projects, 'start_week': start_week, 'end_week': end_week, \
                             'timesheet_form_set': timesheet_form_set, 'week_snapshot_form': week_snapshot_form}
    else:
        TimesheetFormSet = formset_factory(TimesheetForm)
        time_form_set = TimesheetFormSet(request.POST) 
        week_snapshot_form = WeekSnapshotForm(request.POST)
        
        print time_form_set.is_valid()
        if time_form_set.is_valid():
            print time_form_set.cleaned_data
        else:
            print time_form_set.errors
        
        if week_snapshot_form.is_valid():
            print week_snapshot_form.cleaned_data
        else:
            print week_snapshot_form.errors
        
        print request.POST
