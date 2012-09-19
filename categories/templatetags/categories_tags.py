'''
Created on Sep 17, 2012

@author: staticfish
'''
from django import template
from categories.models import TimeOffType
from django.db.models import Q

register = template.Library()

@register.inclusion_tag('snippets/dropdown.html')
def timeoff_options(selected_option=None):
    options = TimeOffType.objects.filter(Q(active=True) & Q(booking_required=True))
    if selected_option:
        options = options.filter(id=selected_option)
        
    return {'options': options, 'selected_option': selected_option, 'dropdown_label': 'Time Off'}
