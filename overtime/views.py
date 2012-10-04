from workflow.models import ApproverQueue
from configuration.models import UserOverTimePolicy
from rules.validators import GenericAspect

def weeksnapshot_post_final_status_update(sender, **kwargs):
    '''
    Called when weeksnapshot is updated with final status. It could be either approved or denied and only updates on approval
    '''
    if kwargs['status'] == ApproverQueue.approved_status():
        weeksnapshot = kwargs['instance']
        #check if user has overtime policy set
        user_overtime_policy = UserOverTimePolicy.objects.get(user_profile=weeksnapshot.user.get_profile())
        if user_overtime_policy:
            #get the ruleset and run thru the validation
            conditions = user_overtime_policy.overtime_policy.overtime_policy_conditions.all()
            for condition in conditions:
                validated_instance = GenericAspect.validate((condition.ruleset,), weeksnapshot)
                if not validated_instance.has_errors:
                    if condition.bank:
                        print 'banking '
                    else:
                        print 'you better pay $'
                    
                    delta = validated_instance.total_hours[3] - validated_instance.total_hours[2]
                    print delta * condition.pay_code.multiplier                
            
