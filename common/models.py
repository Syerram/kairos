"""Stores common dropdown lists"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Q

class Dropdown(models.Model):
    name = models.CharField(_('name'), max_length=20)
    category = models.CharField(_('category'), max_length=5)
    description = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name

admin.site.register(Dropdown)

class DropdownValueManager(models.Manager):
    
    def dropdownvalues(self, category):
        return self.get_query_set().filter(dropdown__category=category)

    def dropdownvalue(self, category, code):
        return self.get_query_set().get(Q(dropdown__category=category) & Q(code=code))

class DropdownValue(models.Model):
    dropdown = models.ForeignKey(Dropdown)
    display = models.CharField(_('Display'), max_length=25)
    code = models.CharField(_('Code'), max_length=5)

    objects = DropdownValueManager()
    
    def __unicode__(self):
        return self.display


admin.site.register(DropdownValue)
