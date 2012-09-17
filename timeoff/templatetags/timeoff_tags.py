'''
Created on Sep 15, 2012

@author: staticfish
'''

from django import template
from kairos.util import throwaway_code
from django.contrib.auth.models import User
register = template.Library()

@register.inclusion_tag('snippets/users_list.html')
@throwaway_code
def user_list(*args, **kwargs):
    """Returns users that are active"""
    return {'users', User.objects.filter(is_active=True)}
