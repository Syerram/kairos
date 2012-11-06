'''
Created on Oct 25, 2012

@author: staticfish
'''
from django.conf.urls import patterns, url
from views import weekly_view

urlpatterns = patterns('',
    #timesheet
    url(r'^(?P<year>\d+)/(?P<week>\d+)/$', weekly_view, name='weekly_view'),                       
    )