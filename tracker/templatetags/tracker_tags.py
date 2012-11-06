"""Timetracking tags"""
from django import template
from datetime import datetime, date, timedelta
import pytz
from workflow.models import ApproverQueue
from categories.views import activities_fetch

register = template.Library()

def day_plus(start_date=None, day_increment=1):
    """adds day to the given date. if none is given it will use current date
    """
    if not start_date:
        start_date = datetime.now()
        
    return start_date + timedelta(days=int(day_increment))

def is_in_future(date=None):
    """Checks whether the data provided, if any, is in future."""
    if not date:
        date = datetime.now()
        return False
    
    date_1 = pytz.UTC.localize(datetime.now())    
    return date > date_1

def monday_of_week(week, year=None):
    """Returns monday of the given week number"""
    if not year:
        year = date.today().year
        
    d = pytz.UTC.localize(datetime(year, 1, 4)) #4 is for falls in first week of the year
    
    return d + timedelta(weeks=week - 1, days= -d.weekday()) 

def is_editable(weeksnapshot_status):
    """its editable if its in draft mode or rejected mode"""
    return weeksnapshot_status.code in (ApproverQueue.draft_status().code, ApproverQueue.rejected_status().code)

def total_hours(weeksnapshot):
    """provides total hours for the week"""
    total_hours = 0
    if weeksnapshot.pk:
        for timesheet in weeksnapshot.timesheets.all():
            total_hours += timesheet.total_hours
    
    return "%0.2f" % (total_hours,)

def total_hours_day(weeksnapshot, day):
    """returns day specific timesheet hours"""
    total_hours = 0
    if weeksnapshot.pk:
        for timesheet in weeksnapshot.timesheets.all():
            day_prop = 'day_' + str(day) + '_hours'
            total_hours += (getattr(timesheet, day_prop, 0) or 0)  
        
    return "%0.2f" % (total_hours,)

@register.inclusion_tag('snippets/dd-refresh.html')
def activity_dropdown(project_id, selected_activity=None):
    return activities_fetch(project_id, selected_activity)

def is_approved(weeksnapshot):
    return weeksnapshot.last_status == ApproverQueue.approved_status()

register.filter("day_plus", day_plus)
register.filter("is_editable", is_editable)
register.assignment_tag(total_hours)
register.simple_tag(total_hours_day)
register.filter("is_in_future", is_in_future)
register.filter("monday_of_week", monday_of_week)
register.filter("is_approved", is_approved)
