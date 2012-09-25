'''
Created on Sep 1, 2012

@author: staticfish
'''
from django.dispatch.dispatcher import Signal
from workflow.views import post_attach_queue_save
from tracker import views as tracker_views
from tracker.models import WeekSnapshot
from timeoff import views as timeoff_views
from timeoff.models import BookTimeOff

post_attach_queue_save_event = Signal(providing_args=['instance', 'is_draft'])
post_attach_queue_save_event.connect(post_attach_queue_save, dispatch_uid='#weeksnapshot#')

post_final_status_event = Signal(providing_args=['instance', 'status'])
post_final_status_event.connect(tracker_views.post_final_status_update, sender=WeekSnapshot, dispatch_uid='#weeksnapshot_approverqueue#')
post_final_status_event.connect(timeoff_views.post_final_status_update, sender=BookTimeOff, dispatch_uid='#booktimeoff_approverqueue#')