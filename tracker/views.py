# Create your views here.
from django.contrib.auth.decorators import login_required
from kairos.util import render_to_html, determine_period, render_to_html_dict

@login_required
@render_to_html_dict(
                     {'timesheet':'timetracker/timesheet.html',
                      'home-r': 'home.html'
                    })
def current_timesheet(request):
    """
    Current timesheet pulls the current week from the database. 
    if one doesn't exists, it creates in-mem object
    """
    user_projects = request.user.get_profile().projects
    start_week, end_week = determine_period()    
    
    return 'timesheet', {'projects': user_projects, 'start_week': start_week, 'end_week': end_week}