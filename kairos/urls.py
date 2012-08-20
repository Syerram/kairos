from django.conf.urls import patterns, include, url
import traceback
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from configuration.views import user_configure
from tracker.views import timesheet_by_week
from categories.views import activities

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^home/$', user_configure, name='home'),
    url(r'^u/conf/$', user_configure, name='user_projects_configure'),
    url(r'^timesheet/(?P<week>\d+)/$', timesheet_by_week, name='timesheet'),
    
    url(r'^activities/(?P<project_id>\d+)/$', activities, name="activities"),
)



def to_template(request, page_name):
    try:
        return direct_to_template(request, '%s.html' % (page_name,))
    except Exception:
        traceback.print_exc()
        raise Http404
