# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DropdownValues'
        db.delete_table('common_dropdownvalues')

        # Adding model 'DropdownValue'
        db.create_table('common_dropdownvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dropdown', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Dropdown'])),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('common', ['DropdownValue'])


    def backwards(self, orm):
        # Adding model 'DropdownValues'
        db.create_table('common_dropdownvalues', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('dropdown', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Dropdown'])),
        ))
        db.send_create_signal('common', ['DropdownValues'])

        # Deleting model 'DropdownValue'
        db.delete_table('common_dropdownvalue')


    models = {
        'common.dropdown': {
            'Meta': {'object_name': 'Dropdown'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'common.dropdownvalue': {
            'Meta': {'object_name': 'DropdownValue'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'dropdown': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Dropdown']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['common']