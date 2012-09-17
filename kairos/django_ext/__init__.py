from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m, ModelAdmin
from django.contrib.admin import helpers

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
    
    
    
        
    
