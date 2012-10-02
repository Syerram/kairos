from categories.models import Project, Taxonomy, TimeOffType
from common.models import DropdownValue, HolidaySet
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from overtime.models import OvertimePolicy

class UserProfile(models.Model):
    '''
        user profile
    '''
    user = models.ForeignKey(User)
    taxonomy = models.ForeignKey(Taxonomy)
    projects = models.ManyToManyField(Project, verbose_name=_('User Projects'), related_name="user_projects", through='UserProject')    
    configured = models.BooleanField(verbose_name=_('configured'), default=False)
    holiday_set = models.ForeignKey(HolidaySet, related_name="user_holidayset", verbose_name=_('User Holiday set'), default=1)
        
    class Meta:
        unique_together = (("user", "taxonomy"),)
    
    def __unicode__(self):
        return self.user.username 

class UserProject(models.Model):
    """Stores projects for each user"""
    
    user_profile = models.ForeignKey(UserProfile)
    project = models.ForeignKey(Project)
    last_updated = models.DateTimeField(auto_now=True)    
    
    class Meta:        
        unique_together = (("user_profile", "project"),)


class UserTimeOffPolicyManager(models.Manager):
    def policies(self, user, timeoff_id=None):
        policy_qs = self.get_query_set().filter(user_profile=user.get_profile())
        if timeoff_id:
            policy_qs = policy_qs.filter(timeoff_type__id=timeoff_id)
        
        return policy_qs

#TODO: create admin task that would add all users to have the initial policy automatically
class UserTimeOffPolicy(models.Model):
    """Stores user specific policies. It is dup of TimeOffPolicy but specific to a user.
        Admin can create default TimeOffPolicy which then will be applied to user by duplicating it into this object
    """
    user_profile = models.ForeignKey(UserProfile)
    
    timeoff_type = models.ForeignKey(TimeOffType)
    
    effective_date = models.DateTimeField(_('Effective Date'))
    
    starting_balance = models.DecimalField(_('Balance'), max_digits=4, decimal_places=2, default=0)
    starting_balance_type = models.ForeignKey(DropdownValue, related_name='user_balance_types', verbose_name=_('User Balance Carryover Type'))
    
    accrue = models.DecimalField(_('Accrue'), max_digits=4, decimal_places=2, default=0)
    accrue_frequency = models.ForeignKey(DropdownValue, verbose_name=_('User Accrual Frequency'), related_name='user_accrue_type_frequencies')
    
    reset_with = models.DecimalField(_('Reset'), max_digits=4, decimal_places=2, default=0)
    reset_frequency = models.ForeignKey(DropdownValue, verbose_name=_('User Reset Frequency'), related_name='user_reset_type_frequencies')
    
    allow_prorate = models.BooleanField(_('Allow Prorate'), default=False)
    tracked = models.BooleanField(_('Track'), default=True)
    
    max_balance_limit = models.SmallIntegerField(_('Maximum Balance Limit'), default=0)
    max_overdraw_limit = models.PositiveSmallIntegerField(_('Maximum Overdraw Limit'), default=0)
    
    time_remaining = models.DecimalField(_('Time Remaining'), max_digits=4, decimal_places=2, default=0)
        
    objects = UserTimeOffPolicyManager()
    
    class Meta:
        verbose_name = _("User TimeOff Policy")
        verbose_name_plural = _("User TimeOff Policies")
    
    def __unicode__(self):
        return 'Timeoff policy for ' + self.user_profile.user.username + ' on [' + self.timeoff_type.name + ']'
    
    
class UserOverTimePolicy(models.Model):
    """
    Maps to user overtime policies
    """
    user_profile = models.ForeignKey(UserProfile, verbose_name=_('User'), related_name='user_overtime')
    overtime_policy = models.ForeignKey(OvertimePolicy, verbose_name=_('Overtime Policy'), related_name='user_overtime_policies')
    
    banked_hours = models.DecimalField(_('Banked Hours'), max_digits=4, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = _("User Overtime Policy")
        verbose_name_plural = _("User Ovretime Policies")
        
    def __unicode__(self):
        return 'User Overtime policy for ' + self.user_profile.user.username + ' on [' + self.overtime_policy.name + ']'
        
