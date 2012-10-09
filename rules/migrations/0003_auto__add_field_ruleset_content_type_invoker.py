# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RuleSet.content_type_invoker'
        db.add_column('rules_ruleset', 'content_type_invoker',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='invoker_content_type', to=orm['contenttypes.ContentType']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RuleSet.content_type_invoker'
        db.delete_column('rules_ruleset', 'content_type_invoker_id')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rules.jointpoint': {
            'Meta': {'object_name': 'JointPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'property_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'property_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'property_types'", 'to': "orm['common.DropdownValue']"})
        },
        'rules.pointcut': {
            'Meta': {'object_name': 'PointCut'},
            'aggregate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'aggregrate'", 'null': 'True', 'to': "orm['common.DropdownValue']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jointpoint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jointpoint'", 'to': "orm['rules.JointPoint']"}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rule'", 'to': "orm['rules.Rule']"})
        },
        'rules.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'operator_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operator_types'", 'to': "orm['common.DropdownValue']"}),
            'required_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'rules.ruleset': {
            'Meta': {'object_name': 'RuleSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'content_type_invoker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoker_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'pointcuts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pointcuts'", 'symmetrical': 'False', 'to': "orm['rules.PointCut']"}),
            'validator_module': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rules']