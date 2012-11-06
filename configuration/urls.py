'''
Created on Oct 25, 2012

@author: staticfish
'''
from django.conf.urls import patterns, url
from views import user_configure_taxonomy, user_configure_projects, \
    user_timeoff_policy

urlpatterns = patterns('',
                       url(r'(?:/(?P<taxonomy>\d+))?/$', user_configure_taxonomy, name='user_configure_taxonomy'),
                       url(r'proj/$', user_configure_projects, name='user_configure_projects'),
                       url(r'timeoff/(?P<timeoff_policy>\d+)/$', user_timeoff_policy, name='user_timeoff_policy'),
                       )