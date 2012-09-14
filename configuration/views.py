# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html_dict
from categories.models import Taxonomy, Project
from configuration.models import UserProject, UserProfile, UserTimeOffPolicy
from configuration.forms import UserTimeOffPolicyForm
from django.contrib.auth.models import User

@login_required
@render_to_html_dict(
                     {
                      'taxonomy-r':'configuration/user_taxonomy.html',
                      'projects-r':'configuration/user_projects.html',
                      'home-r': 'home.html'
                    })
def user_configure_taxonomy(request, taxonomy=None):
    if taxonomy:
        taxonomy = Taxonomy.objects.get(id=taxonomy)
        
        try:
            user_profile = request.user.get_profile()
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user)
            
        user_profile.taxonomy = taxonomy
        user_profile.save()
        
        return 'projects-r', {'projects': Project.objects.active(taxonomy)}
    else:
        configured = False
        try:
            configured = request.user.get_profile().configured
        except UserProfile.DoesNotExist:
            pass
        
        if not configured:
            return 'taxonomy-r', {'taxonomies': Taxonomy.objects.active()}
        else:
            return 'home-r', {}

@render_to_html_dict(
                     {
                      'taxonomy-r':'configuration/user_taxonomy.html',
                      'home-r': 'home.html'
                    })
def user_configure_projects(request):
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
        return 'taxonomy-r', {'taxonomies': Taxonomy.objects.active()}

@render_to_html_dict(
                     {
                      'user_timeoff_policies':'configuration/user_timeoff.html',
                    })
def user_configure_timeoff_policies(request, user, timeoff=None):
    """ 
        fetches/configures policies for the user.
    """    
    
    if request.method == 'POST':
        user_timeoff_policy_form = UserTimeOffPolicyForm(request.POST)
        if user_timeoff_policy_form.is_valid():
            user_timeoff_policy_form.save()
    
    user_timeoff_policies = UserTimeOffPolicy.objects.policies(User.objects.get(id=user), timeoff)
    return 'user_timeoff_policies', {'policies': user_timeoff_policies}
