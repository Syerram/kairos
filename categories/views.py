# Create your views here.
from categories.models import Project
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict

@login_required
@render_to_html_dict({'activity-dropdown':'snippets/dd-refresh.html', })
def activities(request, project_id):
    activities = []
    try:
        project = Project.objects.get(id=project_id)
        activities = project.activities
    except Project.DoesNotExist:
        pass    
    
    return 'activity-dropdown', {'options': activities} 
