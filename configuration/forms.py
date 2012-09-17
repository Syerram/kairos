'''
Created on Sep 13, 2012

@author: staticfish
'''
from django import forms
from common.models import DropdownValue
from configuration.models import UserTimeOffPolicy

class UserTimeOffPolicyForm(forms.ModelForm):
    
    class Meta:
        model = UserTimeOffPolicy
    
    def __init__(self, *args, **kwargs):
        super(UserTimeOffPolicyForm, self).__init__(*args, **kwargs)
        self.fields['starting_balance_type'].queryset = DropdownValue.objects.dropdownvalues('BALAT')
        self.fields['accrue_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')
        self.fields['reset_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')
