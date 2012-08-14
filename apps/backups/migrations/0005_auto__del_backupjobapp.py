# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BackupJobApp'
        db.delete_table('backups_backupjobapp')

        # Adding M2M table for field app on 'BackupJob'
        db.create_table('backups_backupjob_app', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('backupjob', models.ForeignKey(orm['backups.backupjob'], null=False)),
            ('app', models.ForeignKey(orm['app_registry.app'], null=False))
        ))
        db.create_unique('backups_backupjob_app', ['backupjob_id', 'app_id'])


    def backwards(self, orm):
        # Adding model 'BackupJobApp'
        db.create_table('backups_backupjobapp', (
            ('backup_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.BackupJob'])),
            ('app_backup', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('backups', ['BackupJobApp'])

        # Removing M2M table for field app on 'BackupJob'
        db.delete_table('backups_backupjob_app')


    models = {
        'app_registry.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'app': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_registry.App']", 'symmetrical': 'False'}),
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 14, 0, 0)'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'storage_arguments_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'storage_module_name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['backups']