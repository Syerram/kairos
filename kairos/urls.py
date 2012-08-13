from django.conf.urls import patterns, include, url
import traceback
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', 
    #url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    (r'^home/$', 'kairos.urls.to_template', {'page_name': 'home'}),
    (r'^timesheet/$', 'kairos.urls.to_template', {'page_name': 'timetracker/timesheet'}),
)



def to_template(request, page_name):
    try:
        return direct_to_template(request, '%s.html' % (page_name,))
    except Exception:
        traceback.print_exc()
        raise Http404
