# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workflow'
        db.create_table('fsm_workflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('fsm', ['Workflow'])

        # Adding model 'State'
        db.create_table('fsm_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_starter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_terminator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='states', to=orm['fsm.Workflow'])),
        ))
        db.send_create_signal('fsm', ['State'])

        # Adding M2M table for field roles on 'State'
        db.create_table('fsm_state_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('state', models.ForeignKey(orm['fsm.state'], null=False)),
            ('role', models.ForeignKey(orm['users.role'], null=False))
        ))
        db.create_unique('fsm_state_roles', ['state_id', 'role_id'])

        # Adding model 'Transition'
        db.create_table('fsm_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions', to=orm['fsm.Workflow'])),
            ('from_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions_from', to=orm['fsm.State'])),
            ('to_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions_to', to=orm['fsm.State'])),
        ))
        db.send_create_signal('fsm', ['Transition'])

        # Adding M2M table for field roles on 'Transition'
        db.create_table('fsm_transition_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transition', models.ForeignKey(orm['fsm.transition'], null=False)),
            ('role', models.ForeignKey(orm['users.role'], null=False))
        ))
        db.create_unique('fsm_transition_roles', ['transition_id', 'role_id'])

        # Adding model 'Event'
        db.create_table('fsm_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['fsm.Workflow'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['fsm.State'])),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.DropdownValue'])),
        ))
        db.send_create_signal('fsm', ['Event'])

        # Adding M2M table for field roles on 'Event'
        db.create_table('fsm_event_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['fsm.event'], null=False)),
            ('role', models.ForeignKey(orm['users.role'], null=False))
        ))
        db.create_unique('fsm_event_roles', ['event_id', 'role_id'])

        # Adding model 'WorkflowActivity'
        db.create_table('fsm_workflowactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fsm.Workflow'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('fsm', ['WorkflowActivity'])

        # Adding model 'Participant'
        db.create_table('fsm_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('workflow_activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participants', to=orm['fsm.WorkflowActivity'])),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fsm', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['user', 'workflow_activity']
        db.create_unique('fsm_participant', ['user_id', 'workflow_activity_id'])

        # Adding M2M table for field roles on 'Participant'
        db.create_table('fsm_participant_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm['fsm.participant'], null=False)),
            ('role', models.ForeignKey(orm['users.role'], null=False))
        ))
        db.create_unique('fsm_participant_roles', ['participant_id', 'role_id'])

        # Adding model 'WorkflowEventLog'
        db.create_table('fsm_workfloweventlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['fsm.WorkflowActivity'])),
            ('log_type', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fsm.State'], null=True)),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', null=True, to=orm['fsm.Transition'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', null=True, to=orm['fsm.Event'])),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fsm.Participant'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('fsm', ['WorkflowEventLog'])


    def backwards(self, orm):
        # Removing unique constraint on 'Participant', fields ['user', 'workflow_activity']
        db.delete_unique('fsm_participant', ['user_id', 'workflow_activity_id'])

        # Deleting model 'Workflow'
        db.delete_table('fsm_workflow')

        # Deleting model 'State'
        db.delete_table('fsm_state')

        # Removing M2M table for field roles on 'State'
        db.delete_table('fsm_state_roles')

        # Deleting model 'Transition'
        db.delete_table('fsm_transition')

        # Removing M2M table for field roles on 'Transition'
        db.delete_table('fsm_transition_roles')

        # Deleting model 'Event'
        db.delete_table('fsm_event')

        # Removing M2M table for field roles on 'Event'
        db.delete_table('fsm_event_roles')

        # Deleting model 'WorkflowActivity'
        db.delete_table('fsm_workflowactivity')

        # Deleting model 'Participant'
        db.delete_table('fsm_participant')

        # Removing M2M table for field roles on 'Participant'
        db.delete_table('fsm_participant_roles')

        # Deleting model 'WorkflowEventLog'
        db.delete_table('fsm_workfloweventlog')


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
        'fsm.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.DropdownValue']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Role']", 'symmetrical': 'False', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': "orm['fsm.State']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': "orm['fsm.Workflow']"})
        },
        'fsm.participant': {
            'Meta': {'ordering': "['-disabled', 'workflow_activity', 'user']", 'unique_together': "(('user', 'workflow_activity'),)", 'object_name': 'Participant'},
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Role']", 'null': 'True', 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'workflow_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participants'", 'to': "orm['fsm.WorkflowActivity']"})
        },
        'fsm.state': {
            'Meta': {'ordering': "['-is_starter', 'is_terminator']", 'object_name': 'State'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_starter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Role']", 'symmetrical': 'False', 'blank': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': "orm['fsm.Workflow']"})
        },
        'fsm.transition': {
            'Meta': {'object_name': 'Transition'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'from_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions_from'", 'to': "orm['fsm.State']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Role']", 'symmetrical': 'False', 'blank': 'True'}),
            'to_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions_to'", 'to': "orm['fsm.State']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': "orm['fsm.Workflow']"})
        },
        'fsm.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'fsm.workflowactivity': {
            'Meta': {'object_name': 'WorkflowActivity'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fsm.Workflow']"})
        },
        'fsm.workfloweventlog': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'WorkflowEventLog'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'null': 'True', 'to': "orm['fsm.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_type': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fsm.Participant']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fsm.State']", 'null': 'True'}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'null': 'True', 'to': "orm['fsm.Transition']"}),
            'workflow_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['fsm.WorkflowActivity']"})
        },
        'users.role': {
            'Meta': {'ordering': "['name']", 'object_name': 'Role'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['fsm']