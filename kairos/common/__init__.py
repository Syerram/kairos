from kairos.util import enum
from django.utils.translation import ugettext_lazy as _

WORKFLOW_STATUS = enum('DEFINITION', 'ACTIVE', 'RETIRED')

WORKFLOW_STATUS_CHOICES = (
                (WORKFLOW_STATUS.DEFINITION, _('In definition')),
                (WORKFLOW_STATUS.ACTIVE, _('Active')),
                (WORKFLOW_STATUS.RETIRED, _('Retired')),
            )

WORKFLOW_LOG = enum('TRANSITION', 'EVENT', 'ROLE')

WORKFLOW_LOG_CHOICES = (
                        (WORKFLOW_LOG.TRANSITION, _('Transition')),
                        (WORKFLOW_LOG.EVENT, _('Event')),
                        (WORKFLOW_LOG.ROLE, _('Role')),
                    )