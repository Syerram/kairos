'''
Created on Sep 13, 2012

@author: staticfish
'''
from django.forms.models import ModelForm
from configuration.models import UserTimeOffPolicy
from django import forms
from common.models import DropdownValue

class UserTimeOffPolicyForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(UserTimeOffPolicyForm, self).__init__(args, kwargs)
        #only filter data related to their types
        self.fields['starting_balance_type'].queryset = DropdownValue.objects.dropdownvalues('BALAT')
        self.fields['accrue_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')
        self.fields['reset_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')
    
    class Meta:
        model = UserTimeOffPolicy        
        widgets = {
                   'user_profile': forms.HiddenInput(),
                 }
    
