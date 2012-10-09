from workflow.models import ApproverQueue
from configuration.models import UserOverTimePolicy
from rules.validators import GenericAspect
from tracker.models import Timesheet, WeekSnapshot
from django.contrib.contenttypes.models import ContentType

def tally(validated_instance, condition, overtime_hours, banked_hours):
    if not validated_instance.has_errors:
        delta = validated_instance.total_work_hours[3] - validated_instance.total_work_hours[2]
    
    overtime_hours += delta
    if condition.bank:
        banked_hours += delta
    
    return overtime_hours, banked_hours                


def weeksnapshot_post_final_status_update(sender, **kwargs):
    """
    Called when weeksnapshot is updated with final status. 
    If banking, it updates the timeoff policy associated with the user's overtime policy.
    If not banking, ??? Lost in thin air
    
    Arguments:
        sender: expected to be `weeksnapshot`
        
    
    """
    if kwargs['status'] == ApproverQueue.approved_status():
        weeksnapshot = kwargs['instance']
        #check if user has overtime policy set
        user_overtime_policy = UserOverTimePolicy.objects.get(user_profile=weeksnapshot.user.get_profile())
        if user_overtime_policy:
            
            timesheet_type = ContentType.objects.get_for_model(Timesheet)
            week_type = ContentType.objects.get_for_model(WeekSnapshot)
                        
            #get the ruleset and run thru the validation
            conditions = user_overtime_policy.overtime_policy.overtime_policy_conditions.all()
            overtime_hours = 0
            banked_hours = 0
            for condition in conditions:
                if condition.ruleset.content_type == timesheet_type:
                    for timesheet in weeksnapshot.timesheets: 
                        if not timesheet.is_timeoff:                                                   
                            validated_instance = GenericAspect.validate((condition.ruleset,), timesheet)
                            overtime_hours, banked_hours = tally(validated_instance, condition, overtime_hours, banked_hours)                                
                elif condition.ruleset.content_type == week_type:
                    validated_instance = GenericAspect.validate((condition.ruleset,), weeksnapshot)
                    overtime_hours, banked_hours = tally(validated_instance, condition, overtime_hours, banked_hours)
            
            #update the user's timeoff policy linked to the overtime. only update if banked 
            if banked_hours:
                user_overtime_policy.bank_user_timeoff_policy.time_remaining += banked_hours
                user_overtime_policy.bank_user_timeoff_policy.save()
                
            #TODO: poor guy, what to do with overtime house and/or if no timeoff policy is set
            
            