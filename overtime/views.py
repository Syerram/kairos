from workflow.models import ApproverQueue
from configuration.models import UserOverTimePolicy

def weeksnapshot_post_final_status_update(sender, **kwargs):
    '''
    Called when weeksnapshot is updated with final status. It could be either approved or denied and only updates on approval
    '''
    if kwargs['status'] == ApproverQueue.approved_status():
        weeksnapshot = kwargs['instance']
        #check if user has overtime policy set
        overtime_policy = UserOverTimePolicy.objects.get(user_profile=weeksnapshot.user.get_profile())
        if overtime_policy:
            #get the ruleset and run thru the validation
            pass
