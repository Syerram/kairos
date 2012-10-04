from django.db import models
from rules.models import RuleSet
from categories.models import PayCodeType
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class OvertimePolicy(models.Model):
    """
        Defines overtime policy
    """
    
    name = models.CharField(_('Name'), max_length=125)
    description = models.TextField(_('Description'), blank=True, null=True)
    active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _("Overtime Policy")
        verbose_name_plural = _("Overtime Policies")
    
    def __unicode__(self):
        return 'Overtime policy ' + self.name
    
admin.site.register(OvertimePolicy)

class OvertimeCondition(models.Model):
    """
        Defines conditions for each overtime policy
    """
    overtime_policy = models.ForeignKey(OvertimePolicy, verbose_name=_('Overtime Policy'), related_name="overtime_policy_conditions")
    ruleset = models.ForeignKey(RuleSet, verbose_name=_('Rule Set'), related_name="overtime_ruleset")
    pay_code = models.ForeignKey(PayCodeType, verbose_name=_('Pay Code Type'), related_name='overtime_paycode_type')
    bank = models.BooleanField(_('Bank'), default=False)
    
    class Meta:
        verbose_name = _("Overtime Condition")
        verbose_name_plural = _("Overtime Conditions")
    
    def __unicode__(self):
        return 'Overtime Condition ' + self.ruleset.name + ' for ' + self.overtime_policy.name

admin.site.register(OvertimeCondition)
