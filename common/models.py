"""Stores common dropdown lists"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Q
from kairos.util import cacher

class Dropdown(models.Model):
    name = models.CharField(_('Name'), max_length=20)
    category = models.CharField(_('Category'), max_length=5)
    description = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    #system based dropdowns are internal and not editable
    system = models.BooleanField(_('System'), default=False)
    
    def __unicode__(self):
        return self.name

admin.site.register(Dropdown)

def dropdown_keygen(*args, **kwargs):
    return args[1] + (args[2] if len(args) > 2 else '')

class DropdownValueManager(models.Manager):
        
    @cacher(key=dropdown_keygen)
    def dropdownvalues(self, category):
        return self.get_query_set().filter(dropdown__category=category)

    @cacher(key=dropdown_keygen)
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


class Holiday(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.CharField(_('Description'), max_length=1000, null=True, blank=True)    
    day = models.DateField(_('Day of the holiday'))

    def __unicode__(self):
        return self.name
    
admin.site.register(Holiday)
    
class HolidaySet(models.Model):
    """Stores different holiday sets """
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'), null=True, blank=True)
    regional_code = models.CharField(_('Regional Code'), max_length=4)
    holidays = models.ManyToManyField(Holiday, verbose_name=_('Holidays'), related_name="holidays")

    active = models.BooleanField(_('Active'), default=True)
    
    def __unicode__(self):
        return self.name
    
admin.site.register(HolidaySet)   
