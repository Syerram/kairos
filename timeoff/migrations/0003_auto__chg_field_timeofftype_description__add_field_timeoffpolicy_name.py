# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TimeOffType.description'
        db.alter_column('timeoff_timeofftype', 'description', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'TimeOffPolicy.name'
        db.add_column('timeoff_timeoffpolicy', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=125),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'TimeOffType.description'
        db.alter_column('timeoff_timeofftype', 'description', self.gf('django.db.models.fields.TextField')(default=None))
        # Deleting field 'TimeOffPolicy.name'
        db.delete_column('timeoff_timeoffpolicy', 'name')


    models = {
        'categories.paycodetype': {
            'Meta': {'object_name': 'PayCodeType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        },
        'common.dropdown': {
            'Meta': {'object_name': 'Dropdown'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'system': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'common.dropdownvalue': {
            'Meta': {'object_name': 'DropdownValue'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'dropdown': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Dropdown']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'timeoff.timeoffpolicy': {
            'Meta': {'object_name': 'TimeOffPolicy'},
            'accrue': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'accrue_frequency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accrue_type_frequencies'", 'to': "orm['common.DropdownValue']"}),
            'allow_prorate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_balance_limit': ('django.db.models.fields.SmallIntegerField', [], {}),
            'max_overdraw_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'reset_frequency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reset_type_frequencies'", 'to': "orm['common.DropdownValue']"}),
            'reset_with': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'starting_balance_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'balance_types'", 'to': "orm['common.DropdownValue']"}),
            'timeoff_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeoff_type'", 'to': "orm['timeoff.TimeOffType']"})
        },
        'timeoff.timeofftype': {
            'Meta': {'object_name': 'TimeOffType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'booking_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'pay_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paycode'", 'to': "orm['categories.PayCodeType']"})
        }
    }

    complete_apps = ['timeoff']