# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserInfo'
        db.create_table(u'pyta_userinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=128, null=True)),
            ('contact_skype', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('contact_jabber', self.gf('django.db.models.fields.EmailField')(max_length=128, null=True)),
            ('contact_other', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'pyta', ['UserInfo'])


    def backwards(self, orm):
        # Deleting model 'UserInfo'
        db.delete_table(u'pyta_userinfo')


    models = {
        u'pyta.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True'}),
            'contact_jabber': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True'}),
            'contact_other': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'contact_skype': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'})
        }
    }

    complete_apps = ['pyta']