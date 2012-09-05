# Create your views here.
from categories.models import Project
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict

@login_required
@render_to_html_dict({'activity-dropdown':'snippets/dd-refresh.html', })
def activities(request, project_id):
    return 'activity-dropdown', activities_fetch(project_id)

def activities_fetch(project_id, selected_activity=None):
    activities = []
    if project_id:
        try:
            project = Project.objects.get(id=project_id)
            activities = project.activities
        except Project.DoesNotExist:
            pass    
    
    return {'options': activities, 'selected_option': selected_activity} 
