'''
Created on Sep 17, 2012

@author: staticfish
'''
from django import template
from categories.models import TimeOffType

register = template.Library()

#TODO: filter only timeoff bookings the user has access to

@register.inclusion_tag('snippets/dropdown.html')
def timeoff_options(booking_required, selected_option=None):
    options = TimeOffType.objects.filter(active=True)
    if booking_required == 'True':
        options = options.filter(booking_required=booking_required)
        
    return {'options': options, 'selected_option': selected_option, 'dropdown_label': 'Time Off'}
