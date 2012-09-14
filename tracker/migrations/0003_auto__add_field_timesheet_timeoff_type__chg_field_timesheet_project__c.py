# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Timesheet.timeoff_type'
        db.add_column('tracker_timesheet', 'timeoff_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_timeoff_type', null=True, to=orm['timeoff.TimeOffType']),
                      keep_default=False)


        # Changing field 'Timesheet.project'
        db.alter_column('tracker_timesheet', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['categories.Project']))

        # Changing field 'Timesheet.activity'
        db.alter_column('tracker_timesheet', 'activity_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['categories.Activity']))
        # Removing M2M table for field user_timeoffs on 'WeekSnapshot'
        db.delete_table('tracker_weeksnapshot_user_timeoffs')


    def backwards(self, orm):
        # Deleting field 'Timesheet.timeoff_type'
        db.delete_column('tracker_timesheet', 'timeoff_type_id')


        # Changing field 'Timesheet.project'
        db.alter_column('tracker_timesheet', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['categories.Project']))

        # Changing field 'Timesheet.activity'
        db.alter_column('tracker_timesheet', 'activity_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['categories.Activity']))
        # Adding M2M table for field user_timeoffs on 'WeekSnapshot'
        db.create_table('tracker_weeksnapshot_user_timeoffs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('weeksnapshot', models.ForeignKey(orm['tracker.weeksnapshot'], null=False)),
            ('usertimeoff', models.ForeignKey(orm['timeoff.usertimeoff'], null=False))
        ))
        db.create_unique('tracker_weeksnapshot_user_timeoffs', ['weeksnapshot_id', 'usertimeoff_id'])


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
        'categories.paycodetype': {
            'Meta': {'object_name': 'PayCodeType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'})
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
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'timeoff.timeofftype': {
            'Meta': {'object_name': 'TimeOffType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'booking_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'pay_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paycode'", 'to': "orm['categories.PayCodeType']"})
        },
        'tracker.timesheet': {
            'Meta': {'object_name': 'Timesheet'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_activity'", 'null': 'True', 'to': "orm['categories.Activity']"}),
            'day': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'day_1_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_2_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_3_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_4_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_5_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_6_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'day_7_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_project'", 'null': 'True', 'to': "orm['categories.Project']"}),
            'timeoff_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_timeoff_type'", 'null': 'True', 'to': "orm['timeoff.TimeOffType']"})
        },
        'tracker.timesheetnote': {
            'Meta': {'object_name': 'TimesheetNote'},
            'day_1_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_2_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_3_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_4_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_5_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_6_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day_7_note': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timesheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Timesheet']"})
        },
        'tracker.weeksnapshot': {
            'Meta': {'object_name': 'WeekSnapshot'},
            'end_week': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_week': ('django.db.models.fields.DateTimeField', [], {}),
            'timesheets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tracker.Timesheet']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'week': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'tracker.weeksnapshothistory': {
            'Meta': {'object_name': 'WeekSnapshotHistory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weeksnapshot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.WeekSnapshot']"}),
            'weeksnapshot_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.DropdownValue']"})
        }
    }

    complete_apps = ['tracker']