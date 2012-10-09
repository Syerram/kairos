'''
Created on Oct 7, 2012

@author: staticfish
'''
from django import template
from datetime import date, datetime
import calendar
from calendar import month_name

register = template.Library()

MONTH_NAMES = list(calendar.month_name)

month_check = lambda m: int(m) if int(m) <= 12 else 1

@register.inclusion_tag('snippets/calendar.html')
def month_calendar(date):
    '''
        Returns a month calendar list of weeks [with nested list of days] for the given date. 
    '''
    today_day = date.today().day
    today_month = date.today().month

    month = date.month
    year = date.year
    current_week = date.isocalendar()[1]
    first_week = datetime(year, month, 1).isocalendar()[1]    
    last_week = datetime(year, month_check(month + 1), 1).isocalendar()[1]
    
    cal = calendar.HTMLCalendar()
    
    return {'month_calendar': cal.monthdayscalendar(int(year), int(month)),
            'month_name': month_name(year, month),
            'year': year, 'month': month, 'current_week': current_week,
            'first_week': first_week, 'last_week': last_week, 'today_day': today_day, 'today_month': today_month}

def month_name(year, month=None):
    '''
    Returns month name for the given month number
    Arguments:
    operator (int): if non zero, it will add to the month to get the month name. negative numbers are allowed
    
    '''
    if not month:
        month = date.today().month
    
    return MONTH_NAMES[month_check(month)]

def month_shift(month, shift=0):
    if isinstance(month, int) or month.isdigit():
        month = int(month) + int(shift)
    else:
        month = MONTH_NAMES.index(month) + int(shift)    
    
    return MONTH_NAMES[month_check(month)]

register.filter('month_name', month_name)
register.filter('month_shift', month_shift)
