# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PassRecoverCode'
        db.create_table('authentication_passrecovercode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('linkCode', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('linkUsed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkExpired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('authentication', ['PassRecoverCode'])


    def backwards(self, orm):
        # Deleting model 'PassRecoverCode'
        db.delete_table('authentication_passrecovercode')


    models = {
        'authentication.passrecovercode': {
            'Meta': {'object_name': 'PassRecoverCode'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkCode': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'linkExpired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkUsed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['authentication']