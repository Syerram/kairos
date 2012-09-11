# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JointPoint'
        db.create_table('rules_jointpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('property_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('property_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='property_types', to=orm['common.DropdownValue'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('rules', ['JointPoint'])

        # Adding model 'Rule'
        db.create_table('rules_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('required_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('operator_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='operator_types', to=orm['common.DropdownValue'])),
        ))
        db.send_create_signal('rules', ['Rule'])

        # Adding model 'PointCut'
        db.create_table('rules_pointcut', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rule', to=orm['rules.Rule'])),
            ('jointpoint', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jointpoint', to=orm['rules.JointPoint'])),
            ('aggregate', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='aggregrate', null=True, to=orm['common.DropdownValue'])),
        ))
        db.send_create_signal('rules', ['PointCut'])

        # Adding model 'RuleSet'
        db.create_table('rules_ruleset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('validator_module', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rules', ['RuleSet'])

        # Adding M2M table for field pointcuts on 'RuleSet'
        db.create_table('rules_ruleset_pointcuts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ruleset', models.ForeignKey(orm['rules.ruleset'], null=False)),
            ('pointcut', models.ForeignKey(orm['rules.pointcut'], null=False))
        ))
        db.create_unique('rules_ruleset_pointcuts', ['ruleset_id', 'pointcut_id'])


    def backwards(self, orm):
        # Deleting model 'JointPoint'
        db.delete_table('rules_jointpoint')

        # Deleting model 'Rule'
        db.delete_table('rules_rule')

        # Deleting model 'PointCut'
        db.delete_table('rules_pointcut')

        # Deleting model 'RuleSet'
        db.delete_table('rules_ruleset')

        # Removing M2M table for field pointcuts on 'RuleSet'
        db.delete_table('rules_ruleset_pointcuts')


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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type'", 'to': "orm['contenttypes.ContentType']"}),
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'pointcuts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pointcuts'", 'symmetrical': 'False', 'to': "orm['rules.PointCut']"}),
            'validator_module': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rules']