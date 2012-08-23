'''
Created on Aug 22, 2012

@author: staticfish
'''
from django.contrib import admin

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    save_on_top = True
    
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status', 'created_on', 'created_by']
    search_fields = ['name', 'description']
    save_on_top = True
    exclude = ['created_on']
    list_filter = ['status']

class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    save_on_top = True

class TransitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'from_state', 'to_state']
    search_fields = ['name', ]
    save_on_top = True
    
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    save_on_top = True
    search_fields = ['name', 'description']

