"""Timetracking tags"""
from django import template
from datetime import datetime, timedelta

register = template.Library()

def day_plus(start_date, day_increment):
    """adds day to the given date. if none is given it will use current date
    """
    if not start_date:
        start_date = datetime.now()
        
    return start_date + timedelta(days=int(day_increment))

register.filter("day_plus", day_plus)