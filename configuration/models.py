from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from categories.models import Project, Taxonomy

class UserProfile(models.Model):
    '''
        user profile
    '''
    user = models.ForeignKey(User)
    taxonomy = models.ForeignKey(Taxonomy)
    projects = models.ManyToManyField(Project, verbose_name=_('User Projects'), related_name="user_projects", through='UserProject')
    timeoff_policies = models.ManyToManyField(UserTimeOffPolicy, verbose_name=_('User TimeOff Policies'), related_name="user_timeoff_policies")
    configured = models.BooleanField(verbose_name=_('configured'), default=False)
    
    class Meta:
        unique_together = (("user", "taxonomy"),)

class UserProject(models.Model):
    """Stores projects for each user"""
    
    user_profile = models.ForeignKey(UserProfile)
    project = models.ForeignKey(Project)
    last_updated = models.DateTimeField(auto_now=True)    
    
    class Meta:        
        unique_together = (("user_profile", "project"),)

class UserTimeOffPolicy(models.Model):
    """Stores user specific policies. It is dup of TimeOffPolicy but specific to a user.
        Admin can create default TimeOffPolicy which then will be applied to user by duplicating it into this object
    """
    user_profile = models.ForeignKey(UserProfile)
    effective_date = models.DateTimeField(_('Effective Date'))
    
    starting_balance = models.DecimalField(_('Starting Balance'), default=0)
    starting_balance_type = models.ForeignKey(DropdownValue, related_name="starting_balance_type", verbose_name=_('Balance Carryover Type'))
    
    accrue = models.DecimalField(_('Accrue'), default=0)
    accrue_frequency = models.ForeignKey(DropdownValue, related_name="accrue_frequency", verbose_name=_('Accrual Frequency'))
    
    reset_with = models.DecimalField(_('Reset'), default=0)
    reset_frequency = models.ForeignKey(DropdownValue, related_name="reset_frequency", verbose_name=_('Reset Frequency'))
    
    allow_prorate = models.BooleanField(_('Allow Prorate'), default=False)
    
    time_remaining = models.DecimalField(_('Time Remaining'), default=0)
    
    class Meta:
        verbose_name = _("User TimeOff Policy")
        verbose_name_plural = _("User TimeOff Policies")
    
    def __unicode__(self):
        return self.user.username + ' for ' + self.timeoff_type.name

#create timeoff-policy history status and monkey patch the UserTimeOffPolicy with last_status, just like timesheet