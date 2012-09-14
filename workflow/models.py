from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from users.models import Role
from Queue import Queue
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from common.models import DropdownValue
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.comments.models import Comment
from django.db.models import Q

"""
Models for workflow management

"""

class QueueManager(models.Manager):
    
    def get_queue_for_model(self, model):
        queue_type = ContentType.objects.get_for_model(model)
        return self.get(content_type=queue_type)
    
    def active(self):
        return self.get_query_set().filter(active=True)
    
class Queue(models.Model):
    """
        Defines the queue for workflow.
        At any time 
        
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    active = models.BooleanField(_('Active'), default=False)
    
    objects = QueueManager()    
    
    class Meta:
        ordering = ['active']
        verbose_name = _('Queue')
        verbose_name_plural = _('Queues')
        
    def __unicode__(self):
        return self.name

admin.site.register(Queue)

class ApproverManager(models.Manager):
    
    def get_next_approver(self, queue, sequence):
        return self.get(Q(queue=queue) & Q(sequence=sequence + 1))
    
    def get_prev_approver(self, queue, sequence):
        return self.get(Q(queue=queue) & Q(sequence=sequence - 1))
    
class Approver(models.Model):
    """
        defines approver sequence for each queue. 
    """
    role = models.ForeignKey(Role)
    sequence = models.PositiveSmallIntegerField(_('Sequence'), default=0)
    queue = models.ForeignKey(Queue)
    final = models.BooleanField(_('Final Approval'), default=False)
    
    objects = ApproverManager()
    
    class Meta:
        ordering = ['sequence']
        verbose_name = _('Approver')
        verbose_name_plural = _('Approvers')
        
    def __unicode__(self):
        return "Queue: " + self.queue.name + ", Role: " + self.role.name + ", Sequence: " + str(self.sequence)

admin.site.register(Approver)


class ApproverQueueManager(models.Manager):
    
    def user_queue(self, user, status=None):
        query_set = self.get_query_set().filter(current_user=user)
        if status:
            query_set = query_set.filter(current_status=status)
        
        return query_set            

class ApproverQueue(models.Model):
    """
        actual instance of Queue and Approver. 
        Stores the content-type, object-id    
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    current_sequence = models.PositiveSmallIntegerField(_('Current Sequence'))
    current_user = models.ForeignKey(User)
    current_status = models.ForeignKey(DropdownValue)
    
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)    
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True, auto_now_add=True)
    
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    
    objects = ApproverQueueManager()
    
    class Meta:   
        ordering = ['object_id', 'last_updated']
        verbose_name = _('Approver Queue')
        verbose_name_plural = _('Approver Queues')
    
    @staticmethod    
    def submitted_status():
        return DropdownValue.objects.dropdownvalue('WF', 'SUBMT')
    
    @staticmethod    
    def in_queue_status():
        return DropdownValue.objects.dropdownvalue('WF', 'INQUE')

    @staticmethod    
    def approved_status():
        return DropdownValue.objects.dropdownvalue('WF', 'APPRD')
    
    @staticmethod    
    def rejected_status():
        return DropdownValue.objects.dropdownvalue('WF', 'REJTD')    
    
    @staticmethod    
    def draft_status():
        return  DropdownValue.objects.dropdownvalue('WF', 'DRAFT')
    
class ApproverQueueHistoryManager(models.Manager):
    
    def history(self, approver_queue=None, user=None):
        query_set = self.get_query_set()
        if approver_queue:
            query_set = query_set.filter(approver_queue=approver_queue)
        if user:
            query_set = query_set.filter(from_user=user)
        
        return query_set.order_by('-created_on')
    
    def get_head(self, approver_queue):
        return self.get(Q(approver_queue=approver_queue) & Q(from_sequence=0) & Q(from_status=ApproverQueue.submitted_status()))

class ApproverQueueHistory(models.Model):
    """History of approval path"""
    
    approver_queue = models.ForeignKey(ApproverQueue)
    
    from_user = models.ForeignKey(User, related_name='from_user')
    from_status = models.ForeignKey(DropdownValue, related_name='from_status')
    from_sequence = models.PositiveSmallIntegerField(_('from sequence'))
    
    to_user = models.ForeignKey(User, related_name='to_user')
    to_status = models.ForeignKey(DropdownValue, related_name='to_user')
    to_sequence = models.PositiveSmallIntegerField(_('to sequence'))
    
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
        
    comment = GenericRelation(Comment, object_id_field="object_pk", null=True, blank=True)
    
    objects = ApproverQueueHistoryManager()
    
    class Meta:
        verbose_name = _('Approver Queue History')        
