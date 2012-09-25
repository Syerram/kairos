from django.db import models
from datetime import date, timedelta
from django.utils.translation import ugettext_lazy as _
from common.models import DropdownValue
from kairos.util import cacher
from django.contrib.auth.models import User
from kairos.util.monkey_patch import decorator as monkey_patch
from django.db.models import Q
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.comments.models import Comment
from categories.models import TimeOffType
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django import forms

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

"""
    TODO: Hack to load admin form. For some reason, this app cannot load Admin form when the Admin class is in admin.py
    The issue relates to importing of objects, and causes circular import issues

"""
class TimeOffPolicyForm(forms.ModelForm):
    
    class Meta:
        model = TimeOffPolicy
    
    def __init__(self, *args, **kwargs):
        super(TimeOffPolicyForm, self).__init__(*args, **kwargs)
        #TODO: consolidate code between TimeOffPolicyForm and UserTimeOffPolicyForm
        self.fields['starting_balance_type'].queryset = DropdownValue.objects.dropdownvalues('BALAT')
        self.fields['accrue_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')
        self.fields['reset_frequency'].queryset = DropdownValue.objects.dropdownvalues('FREQT')

class TimeOffPolicyAdmin(admin.ModelAdmin):
    
    form = TimeOffPolicyForm
    actions = ['copy_to_user_policy', 'copy_to_user_policy_with_defaults']    

    def copy_to_user_policy(self, request, queryset):
        if queryset.count() > 1:
            messages.error(request, "only one selection allowed!")
        else:
            return HttpResponseRedirect("/u/conf/timeoff/" + str(queryset.all()[0].id))
            
        
    def copy_to_user_policy_with_defaults(self, request, queryset):
        pass
    
    copy_to_user_policy.short_description = "Copy to a User Policy"
    copy_to_user_policy_with_defaults.short_description = "Copy & Save to a User Policy with Defaults"

admin.site.register(TimeOffPolicy, TimeOffPolicyAdmin)

"""Models to store user bookings"""
class BookTimeOffManager(models.Manager):
    def bookings(self, user, timeoff_type=None):
        user_booked_timeoffs = self.get_query_set().filter(user=user)
        if timeoff_type:
            user_booked_timeoffs = user_booked_timeoffs.filter(timeoff_type=timeoff_type)        
            
        return user_booked_timeoffs
    
    def bookings_sofar(self, user, start_date=None, end_date=None, timeoff_type=None):
        if not start_date:
            start_date = date.today()
        
        bookings = self.get_query_set().filter(Q(user=user) & Q(start_date__gte=start_date))   
        
        if end_date:
            bookings = bookings.filter(start_date__lte=end_date)
        
        if timeoff_type:
            bookings = bookings.filter(timeoff_type__id=timeoff_type)
        
        return bookings
         
        
class BookTimeOff(models.Model):
    """Booked timeoff by the user"""
    title = models.CharField(_('Title'), max_length=15, null=True, blank=True)
    user = models.ForeignKey(User)
    timeoff_type = models.ForeignKey(TimeOffType, related_name="book_timeoff_type", verbose_name=_('Book TimeOff Type'))
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))
    number_of_days = models.PositiveIntegerField(_('Number of Days'), default=0)
    
    comment = GenericRelation(Comment, object_id_field='object_pk', null=True, blank=True)
    
    objects = BookTimeOffManager()
    
    class Meta:
        verbose_name = _("Book TimeOff")
        verbose_name_plural = _("Book TimeOffs")

class BookTimeOfffHistory(models.Model):
    """History for the booked timeoff by the user"""
    book_timeoff = models.ForeignKey(BookTimeOff, related_name="book_timeoff", verbose_name=_('Booked TimeOff'))
    book_timeoff_status = models.ForeignKey(DropdownValue)
    last_updated = models.DateTimeField(auto_now=True)   
    
    def __unicode__(self):
        return self.book_timeoff.user.username + ' for ' + self.book_timeoff.timeoff_type.name
    
@monkey_patch(BookTimeOff)
class PatchBookTimeOff(object):
    
    def __last_status(self):
        """If it doesn't exists, returns by default DRAFT status"""
        #TODO create settings attribute instead of hardcoding to DRAFT    
        try:
            return BookTimeOfffHistory.objects.filter(Q(book_timeoff=self)).latest(field_name='last_updated')
        except BookTimeOff.DoesNotExist:
            draft_dropdownvalue = DropdownValue.objects.dropdownvalue('WF', 'DRAFT')
            return BookTimeOfffHistory(book_timeoff=self, book_timeoff_status=draft_dropdownvalue)
    
    last_status = property(__last_status)
    
