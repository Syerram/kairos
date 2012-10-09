'''
Created on Oct 6, 2012

@author: staticfish
'''
from django import template
from django.utils import timesince

register = template.Library()

def error_class(form, control_name):
    if form[control_name].errors:
        return 'error'
    return ''
    
def error_message(form, control_name):
    if form[control_name].errors:
        return ''.join(error for error in form[control_name].errors)
    return ''

def timesince_ext(d, threshold=0, now=None):
    '''
    Extends the inbuilt 'timesince' django filter. It replaces the date/time text lile 'years', 'minutes' with shorter version
    
    Arguments:
        d (date): date from which timesince will be calculated
        threshold (int): defines the threshold on time difference. e.g. if 0, will show the time since in entiterity.
                         1 will remove mins, 2 will remove hours, 3 remove days and so on. max value 5 
    '''
    timesince_str = timesince.timesince(d, now)    
    if threshold:
        timesince_str = ','.join(timesince_str.split(',')[:5 - threshold])
    
    return timesince_str


class AssignNode(template.Node):
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def assign(parser, token):
    """
    Assign an expression to a variable in the current context
    
    Syntax: {% assign [name] [value] %}
    """
    
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s tag takes two arguments" % bits[0])
    
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

#    replacements = {'year': 'y', 'month': 'M', 'week': 'w', 'day': 'd', 'hour': 'h', 'minute': 'min'}
#    return reduce(lambda a, kv: a.replace(*kv), replacements.iteritems(), timesince_str)

register.simple_tag(error_class)
register.simple_tag(error_message)
register.filter("timesince_ext", timesince_ext)
register.tag('assign', assign)