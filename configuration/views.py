# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict
from categories.models import Project
from configuration.models import UserProject

@login_required
@render_to_html_dict(
                     {'projects-r':'configuration/user_projects.html',
                      'home-r': 'home.html'
                    })
def user_configure(request):
    if request.method == 'POST':
        user_profile = request.user.get_profile()
        
        project_ids = request.POST['projects'].split(",")
        for project_id in project_ids:
            project = Project.objects.get(id=project_id)
            user_project = UserProject(user_profile=user_profile, project=project)
            user_project.save()
            
        user_profile.configured = True
        user_profile.save()        
        return 'home-r', {}
    else:
        if not request.user.get_profile().configured:
            return 'projects-r', {'projects': Project.objects.active(), 'next': 'some-view-name'}
        else:
            return 'home-r', {}
