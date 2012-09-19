"""Contains utility packages"""
from django.contrib.messages.storage.session import SessionStorage
from django.conf import settings
from datetime import date, datetime, timedelta, time as time_obj
from django.http import HttpRequest
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.core.cache import cache
import hashlib
import types
from django.conf.locale import fa
from django.db.models.fields.related import ForeignKey
import json
from decimal import Decimal


class ExternalMessageRequestStorage(SessionStorage):
    #TODO
    def __init__(self, request, *args, **kwargs):
        super(ExternalMessageRequestStorage, self).__init__(request, *args, **kwargs)
    
    def add(self, level, message, extra_tags=''):
        '''
        prepares the message. uses external file to load the messages
        '''
        KAIROS_MESSAGE_SETTING = u"SINDEO_MESSAGES"
        if message.startswith('sindeo.message'):
            sindeo_messages = getattr(settings, KAIROS_MESSAGE_SETTING, {})
            if message in sindeo_messages:
                message = sindeo_messages[message]
            else:
                message = '{no message found. message 1001}'
        super(ExternalMessageRequestStorage, self).add(level, message, extra_tags)
        
def determine_period(the_date=date.today()):
    """determines the start and end date of the week and returns tuple"""
    start_week = the_date - timedelta(days=the_date.weekday())
    end_week = start_week + timedelta(days=6)
    
    return (start_week, end_week,)
    
    
def enum(*sequential, **named):
    '''
        creates a enum for the passed in list of values.
        The enum created is list of tuples with name as attribute and index as its value.
        Also adds 'values' attribute having tuple of value and index position
    '''
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['values'] = zip(range(len(sequential)), sequential)
    return type('Enum', (), enums)


def check_for_request(*args):
    '''
    ensures the request exists in the parameter list
    '''
    request = None
    for arg in args:
        if isinstance(arg, HttpRequest):
            request = arg
            break
    assert request is not None
    return request

def render_html(html, data, request):
    '''
    helper function to render the response with given data and request.
    wraps the request in RequestContext
    '''
    if data is None:
        data = {}
    return render_to_response(html, data, context_instance=RequestContext(request))

def render_to_html(html, re_direct=False):
    '''
    decorator function for view handlers that renders the given html.
    removes the need for the redundant usage of returning responses, preparing requests etc
    usage: 
    @render_to_html('target.html')
    def target_handler(request):
        #code..
        return {'context_data': data}
    '''
    def render_decorator(func):
        def wrapper(*args, **kwargs):
            if re_direct:
                return redirect(html)
            else:
                return render_html(html, func(*args, **kwargs), check_for_request(*args))

def render_to_html_dict(html):
    '''
    decorator function for the view handlers that renders the html from the given dictionary.
    it also supports redirection by rendering to view.
    usage:
    @render_to_html_dict({'view_1':'view_1.html', 'view_2':'view_2.html'}) 
    def view_handler(request):
        #code
        if view_1_data:
            return 'view_1', view_1_data
        elif view_2_data:
            reutrn 'view_2', view_2_data
    
    usage: for redirect
    @render_to_html_dict({'view_1':{'url':'/url/to/view', redirect=True}})
    '''
    def render_decorator(func):
        def wrapper(*args, **kwargs):
            request = check_for_request(*args)
            html_key, data = func(*args, **kwargs)
            assert html_key in html
            
            view = html[html_key]
            is_redirect = False
            
            if type(view) == type(dict()):
                is_redirect = view['redirect']
                view = view['url']
                
            if is_redirect:
                return redirect(view)
            else:
                return render_html(view, data, request)
            
        return wrapper
    return render_decorator    

def cacher(key, timeout=None):
    """
    Allows value returning methods to cache their data. Uses the settings defined in the `settings.py` file.
    `key` can be a unicode string, a dictionary of function kwargs, or a function itself. the key function will be provided with all of the arguments the original function takes.
    e.g.
    def key_gen(*args, **kwargs):
        #generate key here
    
    @cacher(key=key_gen)
    def cacheable_function(...):
    
    or 
    @cacher(key='some_key')
    def cacheable_function(...):
    
    or 
    @cacher(key={'first_argument'})
    def cacheable_function(first_argument, ..):
    cacher will lookup `first_argument` in **kwargs
    
    """
    def cache_decorator(func):
        def wrapper(*args, **kwargs):
            #check if the passed in key is actually a func
            if isinstance(key, types.FunctionType):
                gen_key = key(*args, **kwargs)
            else:
                gen_key = key
                
            value = cache.get(gen_key)
            if not value:
                print 'no cache hit'
                value = func(*args, **kwargs)
                if timeout:
                    cache.set(gen_key, value, timeout)
                else:
                    cache.set(gen_key, value)
            return value
        
        return wrapper
    return cache_decorator

def throwaway_code(text=None):
    """
        Throwaway decorator that when tagged to functions, will print to the log that it needs to be cleaned up.
        Meant for temporary functions created and not to be forgatten to be removed
    """
    def throwaway_decorator(func):
        def wrapper(*args, **kwargs):
            print 'dont forget to throwaway ' + func
            if text:
                print '--' + text + '--'
            return func(*args, **kwargs)
        return wrapper
    return throwaway_decorator


def instance_to_dict(instance, key_format=None):
    """
        Returns a dictionary containing field names and values for the given instance.
        Also traverses foreign and many-to-many fields
    """
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
                
    key = lambda key:key_format and key_format % key or key
    
    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()
        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        
    return d

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

json.encoder.FLOAT_REPR = lambda o: format(o, '.1f')

def get_type(cls):
    parts = cls.split('.')
    #will return everything except the actual class
    module = '.'.join(parts[:-1])
    #import top module
    m = __import__(module)
    #import the remaining modules and class    
    for part in parts[1:]:
        m = getattr(m, part)
    
    return m    
