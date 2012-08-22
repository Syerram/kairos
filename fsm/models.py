from django.db import models
from django.utils.translation import ugettext_lazy as _
from kairos.common import WORKFLOW_STATUS_CHOICES, WORKFLOW_STATUS, \
    WORKFLOW_LOG_CHOICES
from django.contrib.auth.models import User
from users.models import Role
from common.models import DropdownValue

"""
Defines the finite state machine models

Workflow --> has N States ---> that can Transition ---> depending on a Event ---> managed by WorkflowProcessor ---> that logs WorkflowLog

"""

# Create your models here.
class Workflow(models.Model):
    """    
        Defines a workflow that can achieve a particular goal, e.g. approval of document.
    """
    # can be in 3 states
    # DEFINITION, ACTIVE, RETIRED
    # This allows users to add new workflow or retire ones not needed
    
    name = models.CharField(_('Workflow Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True, null=True)
    status = models.IntegerField(_('Status'), choices=WORKFLOW_STATUS_CHOICES, default=WORKFLOW_STATUS.DEFINITION)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    

class State(models.Model):
    """
        Defines a individual state. basically the node. 
        Another word is status
    """
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_starter = models.BooleanField(_('Is Start State?'), default=False)
    is_terminator = models.BooleanField(_('Is End State?'), default=False)
    
    #workflow foreign key
    workflow = models.ForeignKey(Workflow, related_names='states')
    roles = models.ManyToManyField(Role, blank=True)
    
    class Meta:
        ordering = ['-is_starter', 'is_terminator']
        verbose_name = _('State')
        verbose_name_plural = _('States')
    
    def __unicode(self):
        self.name
     
class Transition(models.Model):
    """Defines the actual flow of state to another state.
       This is something an event will raise [sorta EventState object]    
    """        
    name = models.CharField(_('Transition Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    workflow = models.ForeignKey(Workflow, related_name='transitions')
    from_state = models.ForeignKey(State, related_name='transitions_from')
    to_state = models.ForeignKey(State, related_name='transitions_to')
    
    roles = models.ManyToManyField(Role, blank=True)
    
    class Meta:
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')
    
    def __unicode__(self):
        return self.name

class Event(models.Model):
    """
        Defines the event that raises the transition.
        For e.g. a event will be raised with transition to pending approval when the state is set to submitted for workflow Timesheet.
        In other words, it triggers the actual transition by setting to the next state.
        It will fetch the next state as Transition.get(from_state=<current-state>)
    """
    
    name = models.CharField(_('Event Summary'), max_length=256)    
    description = models.TextField(_('Description'), blank=True, null=True)
    workflow = models.ForeignKey(Workflow, related_name='events', null=True, blank=True)
    #represents the state it needs for this event to be raised
    state = models.ForeignKey(State, related_name='events', null=True, blank=True)
    
    roles = models.ManyToManyField(Role, blank=True)

    event_type = models.ForeignKey(DropdownValue)
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
    
    def __unicode__(self):
        return self.name
    
class WorkflowActivity(models.Model):
    """
        Others will use this model as a reference to attach themselves with the Workflow.
        Has all the methods to start, stop the workflow.
        The referencing model will trigger each new processor on create. 
        
    """
    
    workflow = models.ForeignKey(Workflow)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ('Workflow Processor')

class Participant(models.Model):
    """Defines which user has what roles in the workflow"""
    user = models.ForeignKey(User)
    roles = models.ManyToManyField(Role, null=True)
    workflow_activity = models.ForeignKey(WorkflowActivity, related_name="participants")
    disabled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-disabled', 'workflow_activity', 'user', ]
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')
        unique_together = ('user', 'workflow_activity')
        
class WorkflowEventLog(models.Model):
    """
        Stores the log of events, transitions happened for the given workflow.
        Also sends signals.
        
    """
    workflow_activity = models.ForeignKey(WorkflowActivity, related_name='history')
    log_type = models.IntegerField(_('Log Type'), choices=WORKFLOW_LOG_CHOICES)
    state = models.ForeignKey(State, null=True)
    transition = models.ForeignKey(Transition, null=True, related_name='history')
    event = models.ForeignKey(Event, null=True, related_name='history')
    participant = models.ForeignKey(Participant)
    
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = _('Worflow Log')
        verbose_name_plural = _('Workflow Logs')
