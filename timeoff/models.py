from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import DropdownValue
from django.contrib.auth.models import User

class TimeOffType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    #pay_code
    description = models.TextField(_('Description'))
    booking_required = models.BooleanField(_('Booking Required'), default=True)
    active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _("TimeOff Type")
        verbose_name_plural = _("TimeOff Types")
    
    def __unicode__(self):
        return self.name

class AccrueType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'))
    active = models.BooleanField(_('Active'), default=True)
    frequency = models.ForeignKey(DropdownValue, related_name="frequency", verbose_name=_('Frequency'))
    accrual = models.PositiveSmallIntegerField(_('Accrual'), default=0)
    
    class Meta:
        verbose_name = _("Accrue Type")
        verbose_name_plural = _("Accrue Types")
    
    def __unicode__(self):
        return self.name

#TODO: repitative code, abstract  
class ResetType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'))
    active = models.BooleanField(_('Active'), default=True)
    
    frequency = models.ForeignKey(DropdownValue, related_name="frequency", verbose_name=_('Frequency'))
    reset_with = models.PositiveSmallIntegerField(_('Reset'), default=0)
    
    class Meta:
        verbose_name = _("Reset Type")
        verbose_name_plural = _("Reset Types")
    
    def __unicode__(self):
        return self.name
    
class TimeOffPolicy(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'))
    
    starting_balance = models.DecimalField(_('Starting Balance'))
    accrue_type = models.ForeignKey(AccrueType, related_name='accrue_type', verbose_name=_('Accrue Type'))
    reset_type = models.ForeignKey(ResetType, related_name="reset_type", verbose_name=_('Reset Type'))    
    
    class Meta:
        verbose_name = _("Reset Type")
        verbose_name_plural = _("Reset Types")
    
    def __unicode__(self):
        return self.name
    
class UserTimeOffPolicy(models.Model):
    user = models.ForeignKey(User, related_name="user", verbose_name=_('User'))
    timeoff_policy = models.ForeignKey(TimeOffPolicy, related_name="timeoffpolicy", verbose_name=_('TimeOff Policy'))
    effective_date = models.DateTimeField(_('Effective Date'))
    
    class Meta:
        verbose_name = _("User TimeOff Policy")
        verbose_name_plural = _("User TimeOff Policies")
    
    def __unicode__(self):
        return self.user.username + '.' + self.timeoff_policy.name
    
    
