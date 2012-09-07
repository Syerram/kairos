# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import determine_period, render_to_html_dict
from tracker.forms import WeekSnapshotForm, TimesheetForm
from tracker.models import WeekSnapshot, Timesheet
from tracker.templatetags.tracker_tags import current_week_number, monday_of_week
from django.forms.models import modelformset_factory
from workflow.signals import post_attach_queue_save_event

@login_required
@render_to_html_dict(
                     {'timesheet':'timetracker/timesheet.html',
                      'home-r': 'home.html'
                    })
def timesheet_by_week(request, week=None):
    """
    Current timesheet pulls the current week from the database. 
    if one doesn't exists, it creates in-mem object.
    If Post, saves it to the database
    """
    if not week:
        week = current_week_number()
    
    if request.method == 'GET':
        user_projects = request.user.get_profile().projects
        start_week, end_week = determine_period(monday_of_week(week)) 
        extra_form = 1
        
        week_snapshot, timesheets = WeekSnapshot.objects.in_period(week, request.user)
        
        if not week_snapshot:
            week_snapshot = WeekSnapshot(user=request.user, week=week, start_week=start_week, end_week=end_week)
        else:
            extra_form = 0
            
        week_snapshot_form = WeekSnapshotForm(prefix="week_snapshot", instance=week_snapshot)
        
        TimesheetFormSet = modelformset_factory(Timesheet, can_delete=True, extra=extra_form, form=TimesheetForm)
        timesheet_form_set = TimesheetFormSet(queryset=timesheets)
        
        return 'timesheet', {'projects': user_projects, 'week': int(week), 'timesheet_form_set': timesheet_form_set, \
                             'week_snapshot': week_snapshot, 'week_snapshot_form': week_snapshot_form}
    else:
        is_draft = request.POST['is_draft'] == 'true'
        
        week_snapshot = WeekSnapshot.objects.get_or_none(week=week, user=request.user)
        week_snapshot_form = WeekSnapshotForm(request.POST, prefix="week_snapshot", instance=week_snapshot)
        if week_snapshot_form.is_valid():
            week_snapshot = week_snapshot_form.save(request.user)
        
        TimesheetFormSet = modelformset_factory(Timesheet, can_delete=True)    
        timesheet_form_set = TimesheetFormSet(request.POST)
        if timesheet_form_set.is_valid():
            timsheets = timesheet_form_set.save()
            week_snapshot.timesheets.clear()
            for timesheet in timsheets:
                week_snapshot.timesheets.add(timesheet)
            week_snapshot.save()
        else:
            print 'raise errors'
             
        #send signal since everything is done correctly
        post_attach_queue_save_event.send(sender=WeekSnapshot, instance=week_snapshot, is_draft=is_draft)
            
        return 'home-r', {}
