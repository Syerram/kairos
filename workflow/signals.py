'''
Created on Sep 1, 2012

@author: staticfish
'''
from django.dispatch.dispatcher import Signal
from workflow.views import post_attach_queue_save

post_attach_queue_save_event = Signal(providing_args=['instance', 'is_draft'])
post_attach_queue_save_event.connect(post_attach_queue_save, dispatch_uid='#weeksnapshot#')