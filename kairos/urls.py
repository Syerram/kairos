from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import Http404, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views

from categories.views import activities
from configuration.views import user_configure_taxonomy
import traceback

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
    url(r'^reports/$', direct_to_template, {'template': 'reports/main.html'}),
    url(r'^activities/(?P<project_id>\d+)/$', activities, name="activities"),
    
    #configuration
    (r'^u/conf/', include('configuration.urls')),    
    (r'^timesheet/', include('tracker.urls')),
    (r'^timeoff/', include('timeoff.urls')),
    (r'^q/', include('workflow.urls')),
    
)


def to_template(request, page_name):
    try:
        return direct_to_template(request, '%s.html' % (page_name,))
    except Exception:
        traceback.print_exc()
        raise Http404
