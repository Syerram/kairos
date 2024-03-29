# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('configuration_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('taxonomy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Taxonomy'])),
            ('configured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('holiday_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_holidayset', to=orm['common.HolidaySet'])),
        ))
        db.send_create_signal('configuration', ['UserProfile'])

        # Adding unique constraint on 'UserProfile', fields ['user', 'taxonomy']
        db.create_unique('configuration_userprofile', ['user_id', 'taxonomy_id'])

        # Adding model 'UserProject'
        db.create_table('configuration_userproject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.UserProfile'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Project'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('configuration', ['UserProject'])

        # Adding unique constraint on 'UserProject', fields ['user_profile', 'project']
        db.create_unique('configuration_userproject', ['user_profile_id', 'project_id'])

        # Adding model 'UserTimeOffPolicy'
        db.create_table('configuration_usertimeoffpolicy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.UserProfile'])),
            ('effective_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('starting_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2)),
            ('starting_balance_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_balance_types', to=orm['common.DropdownValue'])),
            ('accrue', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2)),
            ('accrue_frequency', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_accrue_type_frequencies', to=orm['common.DropdownValue'])),
            ('reset_with', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2)),
            ('reset_frequency', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_reset_type_frequencies', to=orm['common.DropdownValue'])),
            ('allow_prorate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_remaining', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2)),
            ('max_balance_limit', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('max_overdraw_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('configuration', ['UserTimeOffPolicy'])

        # Adding model 'UserTimeOffPolicyHistory'
        db.create_table('configuration_usertimeoffpolicyhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_timeoff_policy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_timeoff_policy', to=orm['configuration.UserTimeOffPolicy'])),
            ('user_timeoff_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.DropdownValue'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('configuration', ['UserTimeOffPolicyHistory'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserProject', fields ['user_profile', 'project']
        db.delete_unique('configuration_userproject', ['user_profile_id', 'project_id'])

        # Removing unique constraint on 'UserProfile', fields ['user', 'taxonomy']
        db.delete_unique('configuration_userprofile', ['user_id', 'taxonomy_id'])

        # Deleting model 'UserProfile'
        db.delete_table('configuration_userprofile')

        # Deleting model 'UserProject'
        db.delete_table('configuration_userproject')

        # Deleting model 'UserTimeOffPolicy'
        db.delete_table('configuration_usertimeoffpolicy')

        # Deleting model 'UserTimeOffPolicyHistory'
        db.delete_table('configuration_usertimeoffpolicyhistory')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'categories.activity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Activity'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'categories.client': {
            'Meta': {'object_name': 'Client'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phone_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'categories.project': {
            'Meta': {'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activities'", 'symmetrical': 'False', 'through': "orm['categories.ProjectActivity']", 'to': "orm['categories.Activity']"}),
            'data_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'project_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'project_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Taxonomy']"})
        },
        'categories.projectactivity': {
            'Meta': {'object_name': 'ProjectActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity'", 'to': "orm['categories.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project'", 'to': "orm['categories.Project']"})
        },
        'categories.taxonomy': {
            'Meta': {'object_name': 'Taxonomy'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        },
        'configuration.userprofile': {
            'Meta': {'unique_together': "(('user', 'taxonomy'),)", 'object_name': 'UserProfile'},
            'configured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'holiday_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_holidayset'", 'to': "orm['common.HolidaySet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_projects'", 'symmetrical': 'False', 'through': "orm['configuration.UserProject']", 'to': "orm['categories.Project']"}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Taxonomy']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'configuration.userproject': {
            'Meta': {'unique_together': "(('user_profile', 'project'),)", 'object_name': 'UserProject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Project']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.UserProfile']"})
        },
        'configuration.usertimeoffpolicy': {
            'Meta': {'object_name': 'UserTimeOffPolicy'},
            'accrue': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'accrue_frequency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_accrue_type_frequencies'", 'to': "orm['common.DropdownValue']"}),
            'allow_prorate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'effective_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_balance_limit': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'max_overdraw_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'reset_frequency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_reset_type_frequencies'", 'to': "orm['common.DropdownValue']"}),
            'reset_with': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'starting_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'starting_balance_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_balance_types'", 'to': "orm['common.DropdownValue']"}),
            'time_remaining': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.UserProfile']"})
        },
        'configuration.usertimeoffpolicyhistory': {
            'Meta': {'object_name': 'UserTimeOffPolicyHistory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_timeoff_policy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_timeoff_policy'", 'to': "orm['configuration.UserTimeOffPolicy']"}),
            'user_timeoff_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.DropdownValue']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['configuration']