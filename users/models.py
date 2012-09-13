from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# Create your models here.
class Role(models.Model):
    """Defines custom role for users. 
    Groups isn't sufficient since you could have 2 people in the same group 
        e.g. Devs but have different roles like Tech Lead and Dev
    """ 
    name = models.CharField(_('Name of Role'), max_length=50)
    description = models.TextField(_('Description'), blank=True, null=True)
    active = models.BooleanField(_('Active'), default=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        """Used in admin"""
        ordering = ['name', ]
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

admin.site.register(Role)