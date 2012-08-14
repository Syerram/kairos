from django.db import models

# Create your models here.
"""Stores common dropdown lists"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

class DropdownModel(models.Model):
    name = models.CharField(_('name'), max_length=20)
    category = models.CharField(_('category'), max_length=5)
    description = models.CharField( max_length=20, null=True)
    active = models.BooleanField(default=True)
        
    def __unicode__(self):
        return self.name
