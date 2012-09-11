from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import DropdownValue

class TimeOffType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    #pay_code
    description = models.TextField(_('Description'))
    booking_required = models.BooleanField(_('Booking Required'), default=True)
    pay_code = models.ForeignKey(PayCodeType, related_name="paycode", verbose_name=_('Pay Code'))
    active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _("TimeOff Type")
        verbose_name_plural = _("TimeOff Types")
    
    def __unicode__(self):
        return self.name

class TimeOffPolicy(models.Model):
    """Defines default time off policy"""
    
    timeoff_type = models.ForeignKey(TimeOffType, related_name="timeoff_type", verbose_name=_('TimeOff Type'))
    
    starting_balance_type = models.ForeignKey(DropdownValue, related_name="starting_balance_type", verbose_name=_('Balance Carryover Type'))
    
    accrue = models.DecimalField(_('Accrue'), default=0)
    accrue_frequency = models.ForeignKey(DropdownValue, related_name="accrue_frequency", verbose_name=_('Accrual Frequency'))
    
    reset_with = models.DecimalField(_('Reset'), default=0)
    reset_frequency = models.ForeignKey(DropdownValue, related_name="reset_frequency", verbose_name=_('Reset Frequency'))
    
    allow_prorate = models.BooleanField(_('Allow Prorate'), default=False)
    
    class Meta:
        verbose_name = _("TimeOff Policy")
        verbose_name_plural = _("TimeOff Policies")
    
    def __unicode__(self):
        return 'System level setup for ' + self.timeoff_type.name
    
    
