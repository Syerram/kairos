# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Holiday.day'
        db.alter_column('common_holiday', 'day', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Holiday.day'
        db.alter_column('common_holiday', 'day', self.gf('django.db.models.fields.DateTimeField')())

    models = {
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
        'common.holiday': {
            'Meta': {'object_name': 'Holiday'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        },
        'common.holidayset': {
            'Meta': {'object_name': 'HolidaySet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holidays': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'holidays'", 'symmetrical': 'False', 'to': "orm['common.Holiday']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'regional_code': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['common']