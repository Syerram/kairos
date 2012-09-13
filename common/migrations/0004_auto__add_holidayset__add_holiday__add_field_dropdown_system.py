# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HolidaySet'
        db.create_table('common_holidayset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('regional_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('common', ['HolidaySet'])

        # Adding M2M table for field holidays on 'HolidaySet'
        db.create_table('common_holidayset_holidays', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('holidayset', models.ForeignKey(orm['common.holidayset'], null=False)),
            ('holiday', models.ForeignKey(orm['common.holiday'], null=False))
        ))
        db.create_unique('common_holidayset_holidays', ['holidayset_id', 'holiday_id'])

        # Adding model 'Holiday'
        db.create_table('common_holiday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('day', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('common', ['Holiday'])

        # Adding field 'Dropdown.system'
        db.add_column('common_dropdown', 'system',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'HolidaySet'
        db.delete_table('common_holidayset')

        # Removing M2M table for field holidays on 'HolidaySet'
        db.delete_table('common_holidayset_holidays')

        # Deleting model 'Holiday'
        db.delete_table('common_holiday')

        # Deleting field 'Dropdown.system'
        db.delete_column('common_dropdown', 'system')


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
            'day': ('django.db.models.fields.DateTimeField', [], {}),
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