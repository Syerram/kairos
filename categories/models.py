from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from users.models import Role
from django.contrib.auth.models import User
from django.db.models import Q
from common.models import DropdownValue

class Rate(models.Model):
    """
        Define rates
    """
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'), null=True, blank=True)
    rate = models.DecimalField(_('Rate'), default=0, decimal_places=2, max_digits=10)
    rate_type = models.ForeignKey(DropdownValue, verbose_name=_('Rate Denominator'), related_name="rate_types")
    currency = models.ForeignKey(DropdownValue, verbose_name=_('Currency'), related_name='currencies')
    
    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')
        
    def __unicode__(self):
        return self.name
    
admin.site.register(Rate)

class Client(models.Model):
    
    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    
    phone_1 = models.IntegerField(blank=True, null=True)
    phone_2 = models.IntegerField(blank=True, null=True)
    fax = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

admin.site.register(Client)

class TaxonomyManager(models.Manager):
    
    def active(self):
        return self.get_query_set().filter(active=True)

class Taxonomy(models.Model):
    """Represents a categorization smaller than client but higher than Project. e.g. Team or Product"""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    client = models.ForeignKey(Client)
    
    objects = TaxonomyManager()
    
    def __unicode__(self):
        return self.name

admin.site.register(Taxonomy)

class TaxonomyRole(models.Model):
    """Defines Taxonomy roles"""
    
    role = models.ForeignKey(Role, verbose_name='Role')
    user = models.ForeignKey(User)
    taxonomy = models.ForeignKey(Taxonomy)
    
    class meta:
        unique_together = ('taxonomy', 'role', 'user')
        verbose_name = _("Taxonomy Role")
        verbose_name_plural = _("Taxonomy Roles")
    
    def __unicode__(self):
        return 'Taxonomy: ' + self.taxonomy.name + ", Role: " + self.role.name + ", User: " + self.user.username

admin.site.register(TaxonomyRole)

class Activity(models.Model):
    code = models.CharField(_('Activity Code'), max_length=5, unique=True)
    name = models.CharField(_('Activity Name'), max_length=50)
    billable = models.BooleanField(_('Billable'), default=False)

    class Meta:
        verbose_name_plural = "activities"
        ordering = ['name']

    def __unicode__(self):
        return self.name

admin.site.register(Activity)

class ProjectManager(models.Manager):
    
    def active(self, taxonomy):
        return self.get_query_set().filter(Q(active=True) & Q(taxonomy=taxonomy))

class Project(models.Model):
    
    taxonomy = models.ForeignKey(Taxonomy)
    name = models.CharField(_('Name'), max_length=10)
    description = models.TextField(blank=True, null=True)
    project_code = models.CharField(max_length=5)
    project_url = models.URLField(blank=True, null=True)
    project_rate = models.ForeignKey(Rate, verbose_name='Rate', related_name='rates', blank=True, null=True)
    
    data_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    active = models.BooleanField(default=True)
    
    activities = models.ManyToManyField(Activity, verbose_name=_('activities'), related_name="activities", through='ProjectActivity')
    
    objects = ProjectManager()
    
    def __unicode__(self):
        return self.name
    
admin.site.register(Project)

class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, related_name="project", verbose_name=_('project'))
    activity = models.ForeignKey(Activity, related_name="activity")

    class Meta:
        verbose_name = _("Project Activity")
        verbose_name_plural = _("Project Activities")

    def __unicode__(self):
        return 'Project: ' + self.project.name + ", Activity: " + self.activity.name

admin.site.register(ProjectActivity)


class PayCodeType(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(_('Code'), max_length=3)
    multiplier = models.PositiveSmallIntegerField(_('Multiplier'), default=1)
    active = models.BooleanField(_('Active'), default=True)
    
    #TODO lotta of these classes, have same unicode, and active flag that needs to be filtered. create abstract class that takes care of this 
    
    class Meta:
        verbose_name = _("Pay Code")
        verbose_name_plural = _("Pay Codes")
    
    def __unicode__(self):
        return self.name
    
admin.site.register(PayCodeType)


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
        verbose_name = _("Time-Off Type")
        verbose_name_plural = _("Time-Off Types")
    
    def __unicode__(self):
        return self.name

admin.site.register(TimeOffType)
