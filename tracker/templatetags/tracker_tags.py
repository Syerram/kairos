"""Timetracking tags"""
from django import template
from datetime import datetime, timedelta
import pytz

register = template.Library()

def day_plus(start_date=None, day_increment=1):
    """adds day to the given date. if none is given it will use current date
    """
    if not start_date:
        start_date = datetime.now()
        
    return start_date + timedelta(days=int(day_increment))

def week_number(date=None):
    return date.isocalendar()[1]

def is_in_future(date=None):
    if not date:
        date = datetime.now()
        return False
    
    date_1 = pytz.UTC.localize(datetime.now())    
    return date > date_1

def current_week_number():
    return week_number(datetime.now())

def monday_of_week(week, year=None):
    if not year:
        year = datetime.now().timetuple().tm_year
        
    d = pytz.UTC.localize(datetime(year, 1, 4)) #4 is for falls in first week of the year
    
    return d + timedelta(weeks=int(week) - 1, days= -d.weekday()) 

register.filter("day_plus", day_plus)
register.simple_tag(week_number)
register.filter("is_in_future", is_in_future)
register.assignment_tag(current_week_number)
register.filter("monday_of_week", monday_of_week)
