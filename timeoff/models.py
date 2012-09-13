from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import DropdownValue
from categories.models import PayCodeType
from django.contrib import admin
from kairos.util import cacher
from django.contrib.auth.models import User
from kairos.util.monkey_patch import decorator as monkey_patch
from django.db.models import Q
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.comments.models import Comment

class TimeOffType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'), null=True, blank=True)
    booking_required = models.BooleanField(_('Booking Required'), default=True)
    pay_code = models.ForeignKey(PayCodeType, related_name="paycode", verbose_name=_('Pay Code'))
    active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _("TimeOff Type")
        verbose_name_plural = _("TimeOff Types")
    
    def __unicode__(self):
        return self.name

admin.site.register(TimeOffType)

class TimeOffPolicy(models.Model):
    """Defines default time off policy"""
    name = models.CharField(_('Name'), max_length=125)
    
    timeoff_type = models.ForeignKey(TimeOffType, related_name="timeoff_type", verbose_name=_('TimeOff Type'))
    
    starting_balance_type = models.ForeignKey(DropdownValue, related_name='balance_types', verbose_name=_('Balance Carryover Type'))
    
    accrue = models.DecimalField(_('Accrue'), max_digits=4, decimal_places=2, default=0)
    accrue_frequency = models.ForeignKey(DropdownValue, related_name='accrue_type_frequencies', verbose_name=_('Accrue Frequency'))
    
    reset_with = models.DecimalField(_('Reset'), max_digits=4, decimal_places=2, default=0)
    reset_frequency = models.ForeignKey(DropdownValue, related_name='reset_type_frequencies', verbose_name=_('Reset Frequency'))
    
    tracked = models.BooleanField(_('Track'), default=True)
    
    allow_prorate = models.BooleanField(_('Allow Prorate'), default=False)
    
    max_balance_limit = models.SmallIntegerField(_('Maximum Balance Limit'))
    max_overdraw_limit = models.PositiveSmallIntegerField(_('Maximum Overdraw Limit'), default=0)
    
    class Meta:
        verbose_name = _("TimeOff Policy")
        verbose_name_plural = _("TimeOff Policies")
    
    def __unicode__(self):
        return 'System level setup for ' + self.name + ' on timeoff [' + self.timeoff_type.name + ']'
    
    #available values for the starting balance, accrue and reset frequency
    @staticmethod
    @cacher(key='FREQUENCY')
    def frequencies():
        return DropdownValue.objects.dropdownvalue('FREQT')
    
    @staticmethod
    @cacher(key='BALANCE_TYPE')
    def balance_carryover_types():
        return DropdownValue.objects.dropdownvalue('BALAT')

admin.site.register(TimeOffPolicy)

class UserTimeOff(models.Model):
    
    user = models.ForeignKey(User)
    timeoff_type = models.ForeignKey(TimeOffType, related_name="user_timeoff_type", verbose_name=_('User TimeOff Type'))
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))
    
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    
    class Meta:
        verbose_name = _("User TimeOff")
        verbose_name_plural = _("User TimeOffs")

class UserTimeOffHistory(models.Model):
    user_timeoff = models.ForeignKey(UserTimeOff, related_name="user_timeoff", verbose_name=_('User TimeOffs'))
    user_timeoff_status = models.ForeignKey(DropdownValue)
    last_updated = models.DateTimeField(auto_now=True)   
    
    def __unicode__(self):
        return self.user_timeoff.user.username + ' timeoff between ' + self.start_date + \
            ' and ' + self.end_date + ' with status '+ self.weeksnapshot_status.name

@monkey_patch(UserTimeOff)
class PatchUserTimeOff(object):
    
    def __last_status(self):
        """If it doesn't exists, returns by default DRAFT status"""
        #TODO create settings attribute instead of hardcoding to DRAFT    
        try:
            return UserTimeOffHistory.objects.filter(Q(user_timeoff=self)).latest(field_name='last_updated')
        except UserTimeOffHistory.DoesNotExist:
            draft_dropdownvalue = DropdownValue.objects.dropdownvalue('TO', 'DRAFT')
            return UserTimeOffHistory(user_timeoff=self, user_timeoff_status=draft_dropdownvalue)
    
    last_status = property(__last_status)
    
