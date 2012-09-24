from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m, ModelAdmin
from django.contrib.admin import helpers
from django import template
from django.template.context import Context
from inspect import getargspec
from django.template.base import TagHelperNode, Template, generic_tag_compiler
from django.utils.itercompat import is_iterable
from functools import partial

class ModelAdminExt(object):
    
    @staticmethod
    def add_view_ext(request, model_class, model_instance, admin_class=None, data=None):
        """
            renders admin add form by prefilling the data. Note this is different from editing an object. 
            The data can be provided in form of a dictionary that matches to the properties of the underlying object
            
            e.g.
            class Person(models.Model):
                name=models.CharField(max_length=25)
                age=models.PositiveInteger..
                ..
                ..
                
            So you want to prepoluate the add admin form with dictionary like
            {'name': 'Sai', 'age': 30}
        """
        if not data:
            data = {}
        
        if not admin_class:
            admin_class = ModelAdmin
        
        #create the admin class    
        model_admin = admin_class(model_class, admin.site)
        #prepare the ModelForm using model_admin
        ModelForm = model_admin.get_form(request, model_instance)
        #create the instance of ModelForm with the passed in model instance
        form = ModelForm(instance=model_instance)
        
        admin_form = helpers.AdminForm(form, model_admin.get_fieldsets(request, model_instance),
                model_admin.get_prepopulated_fields(request, model_instance),
                model_admin.get_readonly_fields(request, model_instance),
                model_admin=model_admin)
        
        data.update({'original': model_instance, 'adminform': admin_form})
        
        return model_admin.add_view(request, extra_context=data)   
    
    
    
class LibraryExt(template.Library):
    
    def dyna_inclusion_tag(self, file_name_key, context_class=Context, takes_context=False, name=None):
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)

            class InclusionNode(TagHelperNode):

                def render(self, context):
                    resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                    _dict = func(*resolved_args, **resolved_kwargs)
                    if not file_name_key in _dict:
                        raise TypeError('key [' + file_name_key + '] not found in dyna_inclusion_tag')
                    else:
                        file_name = _dict[file_name_key]

                    if not getattr(self, 'nodelist', False):
                        from django.template.loader import get_template, select_template
                        if isinstance(file_name, Template):
                            t = file_name
                        elif not isinstance(file_name, basestring) and is_iterable(file_name):
                            t = select_template(file_name)
                        else:
                            t = get_template(file_name)
                        self.nodelist = t.nodelist
                    new_context = context_class(_dict, **{
                        'autoescape': context.autoescape,
                        'current_app': context.current_app,
                        'use_l10n': context.use_l10n,
                        'use_tz': context.use_tz,
                    })
                    # Copy across the CSRF token, if present, because
                    # inclusion tags are often used for forms, and we need
                    # instructions for using CSRF protection to be as simple
                    # as possible.
                    csrf_token = context.get('csrf_token', None)
                    if csrf_token is not None:
                        new_context['csrf_token'] = csrf_token
                    return self.nodelist.render(new_context)

            function_name = (name or
                getattr(func, '_decorated_function', func).__name__)
            compile_func = partial(generic_tag_compiler,
                params=params, varargs=varargs, varkw=varkw,
                defaults=defaults, name=function_name,
                takes_context=takes_context, node_class=InclusionNode)
            compile_func.__doc__ = func.__doc__
            self.tag(function_name, compile_func)
            return func
        return dec
    
