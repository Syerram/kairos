from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import DropdownValue
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from kairos.util import cacher

# Rules go here
#TODO: have the property_name accept regex based patterns, so we could match multiple attributes

class JointPoint(models.Model):
    name = models.CharField(_('Name'), max_length=125)
    property_name = models.CharField(_('Property Name'), max_length=255)
    property_type = models.ForeignKey(DropdownValue, related_name="property_types", verbose_name=_('Property Type'))
        
    class Meta:
        verbose_name = _("Joint Point")
        verbose_name_plural = _("Joint Points")
    
    def __unicode__(self):
        return self.name

admin.site.register(JointPoint)

class Rule(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    required_value = models.TextField(_('Required Value'), null=True, blank=True)
    operator_type = models.ForeignKey(DropdownValue, related_name="operator_types", verbose_name=_('Operator Type'))
    
    def __operator_type(self):
        return DropdownValue.objects.dropdownvalues('OPTYP')

    operator_types = property(__operator_type)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
        
admin.site.register(Rule)

class PointCut(models.Model):
    description = models.TextField(_('Description'), null=True, blank=True)
    rule = models.ForeignKey(Rule, related_name="rule", verbose_name=_("Rule"))
    jointpoint = models.ForeignKey(JointPoint, related_name="jointpoint", verbose_name=_("Joint Point"))
    #only will apply in case of list of joint_point instance
    aggregate = models.ForeignKey(DropdownValue, related_name="aggregrate", verbose_name=_("Aggregate"), null=True, blank=True)
    
    def __unicode__(self):
        return self.rule.name + " pointcuts @ " + self.jointpoint.name
     
    def __aggregate_type(self):
        return DropdownValue.objects.dropdownvalues('AGTYP')

    aggregate_type = property(__aggregate_type)
    
    class Meta:
        verbose_name = _("Point Cut")
        verbose_name_plural = _("Point Cuts")

admin.site.register(PointCut)


def ruleset_key_gen(*args, **kwargs):
    """generates model key by using app.label and model"""
    return args[1].app_label + '.' + args[1].model    

class RuleSetManager(models.Manager):
    
    @cacher(key=ruleset_key_gen)
    def for_content_type(self, content_type):
        """Call if ContentType is available"""
        return RuleSet.objects.filter(content_type=content_type).filter(active=True).distinct()

    def for_instance(self, instance):
        """Call if instance is available. The fetching of ContentType is cached by Django"""
        return self.for_content_type(ContentType.objects.get_for_model(instance))

class RuleSet(models.Model):
    name = models.TextField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    pointcuts = models.ManyToManyField(PointCut, verbose_name=_('Pointcuts'), related_name="pointcuts")
    content_type = models.ForeignKey(ContentType, related_name="content_type", verbose_name=_('Content Type'))
    validator_module = models.CharField(_('Validator Module'), max_length=255, null=True, blank=True)
    
    active = models.BooleanField(_('Active'), default=False)
    
    objects = RuleSetManager()
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Rule Set")
        verbose_name_plural = _("Rule Sets")

admin.site.register(RuleSet)
