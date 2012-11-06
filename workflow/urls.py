'''
Created on Oct 25, 2012

@author: staticfish
'''
from django.conf.urls import patterns, url
from views import queue, queue_shift, queue_history, approval_history

urlpatterns = patterns('',
                       url(r'$', queue, name='queue'),
                       url(r'(?P<bit>[\+\-])/(?P<id>\d+)/$', queue_shift, name='queue'),
                       url(r'(?P<bit>[\+\-])/(?P<id>\d+)/$', queue_shift, name='queue_shift'),
                       url(r'history/$', queue_history, name="queue_history"),
                       url(r'(?P<id>\d+)/history/$', approval_history, name="approval_history"),
                       )
