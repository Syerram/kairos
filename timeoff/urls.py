'''
Created on Oct 25, 2012

@author: staticfish
'''
from django.conf.urls import patterns, url
from views import timeoff_book, timeoff_bookings, timeoff_left

urlpatterns = patterns('',
                       url(r'book/$', timeoff_book, name='timeoff_book'),
                       url(r'bookings(?:/(?P<start_date>\w+))?/$', timeoff_bookings, name='timeoff_bookings'),
                       url(r'left/(?P<timeoff>\d+)/$', timeoff_left, name='timeoff_left'),
                       )