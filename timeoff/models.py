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
    """    
        Defines the `TimeOffType` for the system. Admins can create different timeoff types such as PTO, Jury Duty, Holiday etc.
        `booking_required`, if true, forces time off approval by user supervisor. e.g. PTO. Non approval types include, Lunch, Holiday 
        `pay_code` basically applies to the payout to be given if any
    """
    
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
    """
        Defines default time off policy. Users can define some initial policies that apply to all users.
        The data is then copied to `UserTimeOffPolicy` as is and then admin can further modify as needed
        
        `starting_balance_type` defines how to handle starting balance. whether start @ 0 and carry over balance
        `starting_balance` balance to start with defined by starting_balance_type
        `accrue` actual accrual number
        `accrue_frequency` is what it means
        `reset_with` is when to reset the value. This can be configured in case of scenarios like `Use it or lose it` or `Carry upto 5` only
        `tracked`, provides information related to how many days/hours left and days/hours taken
        `allow_prorate`, coming soon
        `max_balance_limit` check to make sure that accrue doesn't go beyond this limit
        `max_overdraw_limit` check to make sure user doesn't withdraw more than they should
    
    """
    name = models.CharField(_('Name'), max_length=125)
    
    timeoff_type = models.ForeignKey(TimeOffType, related_name="timeoff_type", verbose_name=_('TimeOff Type'))
    
    starting_balance_type = models.ForeignKey(DropdownValue, related_name='balance_types', verbose_name=_('Balance Carryover Type'))
    starting_balance = models.DecimalField(_('Balance'), max_digits=4, decimal_places=2, default=0)
    
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

class BookTimeOff(models.Model):
    """Booked timeoff by the user"""
    user = models.ForeignKey(User)
    timeoff_type = models.ForeignKey(TimeOffType, related_name="book_timeoff_type", verbose_name=_('Book TimeOff Type'))
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))
    
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    
    class Meta:
        verbose_name = _("Book TimeOff")
        verbose_name_plural = _("Book TimeOffs")

class BookTimeOfffHistory(models.Model):
    """History for the booked timeoff by the user"""
    book_timeoff = models.ForeignKey(BookTimeOff, related_name="book_timeoff", verbose_name=_('Booked TimeOff'))
    book_timeoff_status = models.ForeignKey(DropdownValue)
    last_updated = models.DateTimeField(auto_now=True)   
    
    def __unicode__(self):
        return self.book_timeoff.user.username + ' timeoff between ' + self.start_date + \
            ' and ' + self.end_date + ' with status ' + self.weeksnapshot_status.name

@monkey_patch(BookTimeOff)
class PatchBookTimeOff(object):
    
    def __last_status(self):
        """If it doesn't exists, returns by default DRAFT status"""
        #TODO create settings attribute instead of hardcoding to DRAFT    
        try:
            return BookTimeOff.objects.filter(Q(book_timeoff=self)).latest(field_name='last_updated')
        except BookTimeOff.DoesNotExist:
            draft_dropdownvalue = DropdownValue.objects.dropdownvalue('TO', 'DRAFT')
            return BookTimeOff(book_timeoff=self, book_timeoff_status=draft_dropdownvalue)
    
    last_status = property(__last_status)
