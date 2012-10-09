# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import determine_period, render_to_html_dict
from tracker.forms import WeekSnapshotForm, TimesheetForm
from tracker.models import WeekSnapshot, Timesheet, WeekSnapshotHistory
from tracker.templatetags.tracker_tags import current_week_number, monday_of_week
from django.forms.models import modelformset_factory
import workflow
from workflow.models import ApproverQueue
from rules.models import RuleSet
from rules.validators import GenericAspect
from django.contrib.contenttypes.models import ContentType

#TODO: to be big of a method
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
    #TODO: have submit thru JSON    
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
        status = ApproverQueue.draft_status if is_draft else ApproverQueue.in_queue_status()
        
        week_snapshot = WeekSnapshot.objects.get_or_none(week=week, user=request.user)
        week_snapshot_form = WeekSnapshotForm(request.POST, prefix="week_snapshot", instance=week_snapshot)
        if week_snapshot_form.is_valid():
            week_snapshot = week_snapshot_form.save(request.user)            
        
        TimesheetFormSet = modelformset_factory(Timesheet, can_delete=True)    
        timesheet_form_set = TimesheetFormSet(request.POST)
        
        #Pull rulesets for weeksnapshot
        rulesets = RuleSet.objects.for_invoker_model(WeekSnapshot)
        
        timesheet_rulesets = rulesets.filter(content_type=ContentType.objects.get_for_model(Timesheet))
        week_rulesets = rulesets.filter(content_type=ContentType.objects.get_for_model(WeekSnapshot))
        #TODO: serve the errors through JSON errors
        if timesheet_form_set.is_valid():
            timsheets = timesheet_form_set.save()
            week_snapshot.timesheets.clear()
            #TODO: should batch all of the errors into one and send them back
            for timesheet in timsheets:
                if timesheet_rulesets:
                    validated_instance = GenericAspect.validate(timesheet_rulesets, timesheet)
                    if validated_instance.has_errors:
                        raise TypeError('ruleset errors encountered')
                week_snapshot.timesheets.add(timesheet)
            week_snapshot.save()
        else:
            raise TypeError('validation errors encountered')
        
        #check if we have validators
        if week_rulesets:
            validated_instance = GenericAspect.validate(week_rulesets, week_snapshot)
            if validated_instance.has_errors:
                raise TypeError('ruleset errors encountered')
        
        #add new status to the weeksnapshot
        post_status_update(week_snapshot, status)            
    
        #send signal since everything is done correctly
        workflow.signals.post_attach_queue_save_event.send(sender=WeekSnapshot, instance=week_snapshot, is_draft=is_draft)
            
        return 'home-r', {}
    
def post_status_update(instance, status):
    """
    Helper class to update the `WeekSnapshot` history.
    
    Arguments:
        instance: Expected to be `Weeksnapshot` instance
        status: Status of the timesheet
    """
    weeksnapshot_status = WeekSnapshotHistory(weeksnapshot=instance, weeksnapshot_status=status)
    weeksnapshot_status.save() 
    
def post_final_status_update(sender, **kwargs):
    """
       Event handlers for post final Status 
    
    """
    #TODO: update the name to more meaningful like _event_handler
    post_status_update(kwargs['instance'], kwargs['status']);
    #TODO send email if rejected
