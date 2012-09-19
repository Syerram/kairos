'''
Created on Sep 17, 2012

@author: staticfish
'''
from django import template
from common.models import DropdownValue

register = template.Library()

@register.inclusion_tag('snippets/dropdown.html')
def dropdown(category, category_label, selected_option=None):
    options = DropdownValue.objects.dropdownvalue(category)
    return {'options': options, 'selected_option': selected_option, 'dropdown_label': category_label}