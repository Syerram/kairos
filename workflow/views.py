# Create your views here.
from django.db.models import Q
from workflow.models import ApproverQueue, Queue, Approver, ApproverQueueHistory
from tracker.models import WeekSnapshotHistory
from categories.models import TaxonomyRole
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict

def post_attach_queue_save(sender, **kwargs):
    """
    Creates a weeksnapshot history &
    attaches the Approver-Queue instance to a Weeksnapshot object
    """
    
    is_draft = kwargs['is_draft']
    instance = kwargs['instance']
    status = ApproverQueue.draft_status if is_draft else ApproverQueue.in_queue_status()
    #add new status to the weeksnapshot
    weeksnapshot_status = WeekSnapshotHistory(weeksnapshot=instance, \
                                              weeksnapshot_status=status)            
    weeksnapshot_status.save()
    
    #if not draft, then get next approver queue.
    if(not is_draft):
        queue = Queue.objects.get_queue_for_model(sender)
    
        #add the next user in sequence
        approver_queue = next_approver_in_queue(instance, 0, queue)
        
        #found one, so lets move to the next approver. create approver queue history
        if approver_queue:
            #create a history for approver_queue with the original user 
            #save record with 0 sequence in the history for the submitter
            approver_queue_history = ApproverQueueHistory(
                                      approver_queue=approver_queue,
                                      from_user=instance.user,
                                      from_status=ApproverQueue.submitted_status(),
                                      from_sequence=0,
                                      to_user=approver_queue.current_user,
                                      to_status=approver_queue.current_status,
                                      to_sequence=approver_queue.current_sequence)    
            approver_queue_history.save()  
        
        else:
            weeksnapshot_status = WeekSnapshotHistory(weeksnapshot=instance,
                                                  weeksnapshot_status=ApproverQueue.approved_status())
            weeksnapshot_status.save() 
        
        
def next_approver_in_queue(instance, sequence, queue=None, approver_queue=None):
    """
        gets next approver using the passed in sequence.
        If the approver is last in the sequence, then update target object        
    """ 
    if not queue:
        #fetch Queue first
        queue = Queue.objects.get_queue_for_model(instance)
        
    try:
        approver = Approver.objects.get_next_approver(queue, sequence)
    except Approver.DoesNotExist:
        #last one in the queue, that got approved, update & return none
        if approver_queue:
            approver_queue.current_status = ApproverQueue.approved_status()
            approver_queue.save()
            return approver_queue
        else:
            return None
    
    #create new approver-queue 
    #gather the user using the taxonomy role 
    taxonomy = instance.user.get_profile().taxonomy
    taxonomy_role = TaxonomyRole.objects.get(Q(taxonomy=taxonomy) & Q(role=approver.role))
    
    #If the approver is final then, status will be approved
    status = ApproverQueue.in_queue_status() 
    
    #create a new approver queue if one wasn't passed
    if not approver_queue:
        approver_queue = ApproverQueue(content_object=instance,
                                   content_type=queue.content_type)
        
    approver_queue.current_status = status
    approver_queue.current_user = taxonomy_role.user
    approver_queue.current_sequence = approver.sequence
    approver_queue.save()
    
    return approver_queue


@login_required
@render_to_html_dict({'queue':'workflow/queue.html'})
def queue(request):
    return 'queue', {'queue_items': ApproverQueue.objects.user_queue(request.user, ApproverQueue.in_queue_status())}

@login_required
@render_to_html_dict({'queue_history':'workflow/queue_history.html'})
def queue_history(request):
    return 'queue_history', {'queue_items': ApproverQueueHistory.objects.history(user=request.user)}

@login_required
@render_to_html_dict({'approval_history':'workflow/approval_history.html'})
def approval_history(request, id):
    approver_queue = ApproverQueue.objects.get(id=id)
    return 'approval_history', {'history_items': ApproverQueueHistory.objects.history(approver_queue=approver_queue, user=request.user)}
    
@login_required
@render_to_html_dict({'queue':'workflow/queue.html'})
def queue_shift(request, bit, id):
    """Shifts the queue according to the bit operator"""
    approver_queue = ApproverQueue.objects.get(id=id)
    current_user, current_sequence, current_status = approver_queue.current_user, approver_queue.current_sequence, approver_queue.current_status
    if bit == "+":
        approver_queue = next_approver_in_queue(approver_queue.content_object, \
                                                approver_queue.current_sequence, None, approver_queue)
        
        
        approver_queue_history = ApproverQueueHistory(
                                      approver_queue=approver_queue,
                                      from_user=current_user,
                                      from_status=current_status,
                                      from_sequence=current_sequence,
                                      to_user=approver_queue.current_user,
                                      to_status=approver_queue.current_status,
                                      to_sequence=approver_queue.current_sequence)     
        approver_queue_history.save()  
        
        if approver_queue.current_status == ApproverQueue.approved_status():
            #add history with approved status
            weeksnapshot_status = WeekSnapshotHistory(weeksnapshot=approver_queue.content_object,
                                                  weeksnapshot_status=approver_queue.current_status)
            weeksnapshot_status.save() 
    elif bit == "-":
        #need to send it back to the original submitter
        approver_queue_history_head = ApproverQueueHistory.objects.get_head(approver_queue)
        
        #add a new approver-queue-history
        #TODO: duplicate code, make it generic
        approver_queue_history = ApproverQueueHistory(
                          approver_queue=approver_queue,
                          from_user=current_user,
                          from_status=current_status,
                          from_sequence=current_sequence,
                          to_user=approver_queue_history_head.from_user,
                          to_status=ApproverQueue.rejected_status(),
                          to_sequence=approver_queue_history_head.from_sequence)
        
        approver_queue_history.save()
        
        #update the current approver queue and set it to the original user
        approver_queue.current_status = ApproverQueue.rejected_status()
        approver_queue.current_user = approver_queue_history_head.from_user
        approver_queue.current_sequence = approver_queue_history_head.from_sequence
        approver_queue.save()
        
        #update the weeksnapshot status
        weeksnapshot_status = WeekSnapshotHistory(weeksnapshot=approver_queue.content_object,
                                                  weeksnapshot_status=ApproverQueue.rejected_status())
        weeksnapshot_status.save() 
    
    return 'queue', {'items': ApproverQueue.objects.user_queue(request.user, ApproverQueue.in_queue_status())}
