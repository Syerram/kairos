# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict
from categories.models import Project

@login_required
@render_to_html_dict(
                     {'projects-r':'configuration/user_projects.html',
                      'home-r': 'home.html'
                    })
def user_configure_check(request):
    if not request.user.get_profile().configured:
        return 'projects-r', {'projects': Project.objects.active()}
    else:
        return 'home-r', {}
