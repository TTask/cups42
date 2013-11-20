# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestPriorityEntry'
        db.create_table(u'pyta_requestpriorityentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request_path', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('request_priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'pyta', ['RequestPriorityEntry'])

        # Adding field 'RequestHistoryEntry.request_priority'
        db.add_column(u'pyta_requesthistoryentry', 'request_priority',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'RequestPriorityEntry'
        db.delete_table(u'pyta_requestpriorityentry')

        # Deleting field 'RequestHistoryEntry.request_priority'
        db.delete_column(u'pyta_requesthistoryentry', 'request_priority')


    models = {
        u'pyta.modelhistoryentry': {
            'Meta': {'object_name': 'ModelHistoryEntry'},
            'change_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'pyta.requesthistoryentry': {
            'Meta': {'object_name': 'RequestHistoryEntry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'request_path': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'request_priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'pyta.requestpriorityentry': {
            'Meta': {'object_name': 'RequestPriorityEntry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_path': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'request_priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'pyta.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True'}),
            'contact_jabber': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True'}),
            'contact_other': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'contact_skype': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'})
        }
    }

    complete_apps = ['pyta']