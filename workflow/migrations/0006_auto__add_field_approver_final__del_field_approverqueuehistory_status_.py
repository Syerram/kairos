# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Approver.final'
        db.add_column('workflow_approver', 'final',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'ApproverQueueHistory.status'
        db.delete_column('workflow_approverqueuehistory', 'status_id')

        # Deleting field 'ApproverQueueHistory.prev_user'
        db.delete_column('workflow_approverqueuehistory', 'prev_user_id')

        # Deleting field 'ApproverQueueHistory.prev_sequence'
        db.delete_column('workflow_approverqueuehistory', 'prev_sequence')

        # Adding field 'ApproverQueueHistory.from_user'
        db.add_column('workflow_approverqueuehistory', 'from_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='from_user', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.from_status'
        db.add_column('workflow_approverqueuehistory', 'from_status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='from_status', to=orm['common.DropdownValue']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.from_sequence'
        db.add_column('workflow_approverqueuehistory', 'from_sequence',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.to_user'
        db.add_column('workflow_approverqueuehistory', 'to_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='to_user', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.to_status'
        db.add_column('workflow_approverqueuehistory', 'to_status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='to_user', to=orm['common.DropdownValue']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.to_sequence'
        db.add_column('workflow_approverqueuehistory', 'to_sequence',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None),
                      keep_default=False)

        # Deleting field 'ApproverQueue.status'
        db.delete_column('workflow_approverqueue', 'status_id')

        # Adding field 'ApproverQueue.current_status'
        db.add_column('workflow_approverqueue', 'current_status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['common.DropdownValue']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Approver.final'
        db.delete_column('workflow_approver', 'final')

        # Adding field 'ApproverQueueHistory.status'
        db.add_column('workflow_approverqueuehistory', 'status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['common.DropdownValue']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.prev_user'
        db.add_column('workflow_approverqueuehistory', 'prev_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'ApproverQueueHistory.prev_sequence'
        db.add_column('workflow_approverqueuehistory', 'prev_sequence',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None),
                      keep_default=False)

        # Deleting field 'ApproverQueueHistory.from_user'
        db.delete_column('workflow_approverqueuehistory', 'from_user_id')

        # Deleting field 'ApproverQueueHistory.from_status'
        db.delete_column('workflow_approverqueuehistory', 'from_status_id')

        # Deleting field 'ApproverQueueHistory.from_sequence'
        db.delete_column('workflow_approverqueuehistory', 'from_sequence')

        # Deleting field 'ApproverQueueHistory.to_user'
        db.delete_column('workflow_approverqueuehistory', 'to_user_id')

        # Deleting field 'ApproverQueueHistory.to_status'
        db.delete_column('workflow_approverqueuehistory', 'to_status_id')

        # Deleting field 'ApproverQueueHistory.to_sequence'
        db.delete_column('workflow_approverqueuehistory', 'to_sequence')

        # Adding field 'ApproverQueue.status'
        db.add_column('workflow_approverqueue', 'status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['common.DropdownValue']),
                      keep_default=False)

        # Deleting field 'ApproverQueue.current_status'
        db.delete_column('workflow_approverqueue', 'current_status_id')


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
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'users.role': {
            'Meta': {'ordering': "['name']", 'object_name': 'Role'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'workflow.approver': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'Approver'},
            'final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.Queue']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Role']"}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'workflow.approverqueue': {
            'Meta': {'ordering': "['object_id', 'last_updated']", 'object_name': 'ApproverQueue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.DropdownValue']"}),
            'current_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'workflow.approverqueuehistory': {
            'Meta': {'object_name': 'ApproverQueueHistory'},
            'approver_queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.ApproverQueue']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'from_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_status'", 'to': "orm['common.DropdownValue']"}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'to_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': "orm['common.DropdownValue']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': "orm['auth.User']"})
        },
        'workflow.queue': {
            'Meta': {'ordering': "['active']", 'object_name': 'Queue'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['workflow']