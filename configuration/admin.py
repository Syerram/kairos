'''
Created on Sep 15, 2012

@author: staticfish
'''
from django.contrib import admin
from configuration.models import UserTimeOffPolicy, UserProfile,\
    UserOverTimePolicy
from configuration.forms import UserTimeOffPolicyForm

class UserTimeOffPolicyAdmin(admin.ModelAdmin):
    form = UserTimeOffPolicyForm
        
admin.site.register(UserTimeOffPolicy, UserTimeOffPolicyAdmin)
admin.site.register(UserProfile)
admin.site.register(UserOverTimePolicy)
