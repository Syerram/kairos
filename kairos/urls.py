from django.conf.urls import patterns, include, url
import traceback
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from configuration.views import user_configure_taxonomy, user_configure_projects
from tracker.views import timesheet_by_week
from categories.views import activities
from workflow.views import queue, queue_shift, queue_history, approval_history

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),    
    url(r'^home/$', user_configure_taxonomy, name='home'),
    
    #configuration
    url(r'^u/conf(?:/(?P<taxonomy>\d+))?/$', user_configure_taxonomy, name='user_configure_taxonomy'),
    url(r'^u/conf/proj/$', user_configure_projects, name='user_configure_projects'),
    
    #timesheet
    url(r'^timesheet/(?P<week>\d+)/$', timesheet_by_week, name='timesheet'),
    
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
