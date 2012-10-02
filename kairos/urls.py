from categories.views import activities
from configuration.views import user_configure_taxonomy, user_configure_projects, \
    user_timeoff_policy
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import Http404, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from tracker.views import timesheet_by_week
from workflow.views import queue, queue_shift, queue_history, approval_history
import traceback
from timeoff.views import timeoff_left, timeoff_book, timeoff_bookings
from django.contrib.auth import views

def logout(request):
    views.logout(request)
    next = '/login/'
    if 'next' in request.GET:
        next = request.GET['next']
    
    return HttpResponseRedirect(next)

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^logout/$', logout, name='logout'),
    url(r'^home/$', user_configure_taxonomy, name='home'),
    
    #configuration
    url(r'^u/conf(?:/(?P<taxonomy>\d+))?/$', user_configure_taxonomy, name='user_configure_taxonomy'),
    url(r'^u/conf/proj/$', user_configure_projects, name='user_configure_projects'),
    url(r'^u/conf/timeoff/(?P<timeoff_policy>\d+)/$', user_timeoff_policy, name='user_timeoff_policy'),
    url(r'^u/timeoff/left/(?P<timeoff>\d+)/$', timeoff_left, name='timeoff_left'),
    
    #timesheet
    url(r'^timesheet/(?P<week>\d+)/$', timesheet_by_week, name='timesheet'),
    
    #timeoff booking
    url(r'^timeoff/book/$', timeoff_book, name='timeoff_book'),
    url(r'^timeoff/bookings(?:/(?P<start_date>\w+))?/$', timeoff_bookings, name='timeoff_bookings'),
    
    #Q management
    url(r'^q/$', queue, name='queue'),
    url(r'^q/(?P<bit>[\+\-])/(?P<id>\d+)/$', queue_shift, name='queue'),
    url(r'^q/(?P<bit>[\+\-])/(?P<id>\d+)/$', queue_shift, name='queue_shift'),
    url(r'^q/history/$', queue_history, name="queue_history"),
    url(r'^q/(?P<id>\d+)/history/$', approval_history, name="approval_history"),
    
    #auxillary urls
    url(r'^activities/(?P<project_id>\d+)/$', activities, name="activities"),
    
)


def to_template(request, page_name):
    try:
        return direct_to_template(request, '%s.html' % (page_name,))
    except Exception:
        traceback.print_exc()
        raise Http404
