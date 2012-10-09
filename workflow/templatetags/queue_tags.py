'''
Created on Sep 20, 2012

@author: staticfish
'''
from kairos import django_ext
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from workflow.views import queue_count as q_count
from django.utils import timesince

"""Queue based tags"""


register = django_ext.LibraryExt()

@register.dyna_inclusion_tag('content_snapshot_path')
def content_type_snapshot(queue_item):
    """    
        returns a dictionary of content data and the content html associated with this
    """
    content_type = ContentType.objects.get_for_model(queue_item.content_object)
    content_type_label = '.'.join(content_type.natural_key())
    QUEUE_SNAPSHOT = settings.QUEUE_CONTENT_TYPE_SETTINGS['QUEUE_SNAPSHOT']
    if content_type_label in QUEUE_SNAPSHOT:
        return {'content_snapshot_path': QUEUE_SNAPSHOT[content_type_label], 'queue_item': queue_item}
    
#TODO: consolidate both

@register.dyna_inclusion_tag('content_snapshot_path')
def content_type_history(queue_item_history):
    content_type = ContentType.objects.get_for_model(queue_item_history.approver_queue.content_object)
    content_type_label = '.'.join(content_type.natural_key())
    QUEUE_HISTORY = settings.QUEUE_CONTENT_TYPE_SETTINGS['QUEUE_HISTORY']
    if content_type_label in QUEUE_HISTORY:
        return {'content_snapshot_path': QUEUE_HISTORY[content_type_label], 'queue_item': queue_item_history}

def queue_count(user):
    '''
    Returns the count of the queue waiting for approval
    Arguments: 
        user (User): queue count for the given user
    '''
    return q_count(user)


register.assignment_tag(queue_count)