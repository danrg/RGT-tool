# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Grid'
        db.create_table('gridMng_grid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('dendogram', self.gf('django.db.models.fields.TextField')(null=True)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 1, 0, 0), null=True)),
            ('grid_type', self.gf('django.db.models.fields.CharField')(default='u', max_length=2)),
        ))
        db.send_create_signal('gridMng', ['Grid'])

        # Adding model 'Alternatives'
        db.create_table('gridMng_alternatives', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Grid'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('gridMng', ['Alternatives'])

        # Adding model 'Concerns'
        db.create_table('gridMng_concerns', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Grid'])),
            ('leftPole', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('rightPole', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('gridMng', ['Concerns'])

        # Adding model 'Ratings'
        db.create_table('gridMng_ratings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Concerns'])),
            ('alternative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Alternatives'])),
            ('rating', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('gridMng', ['Ratings'])

        # Adding unique constraint on 'Ratings', fields ['concern', 'alternative']
        db.create_unique('gridMng_ratings', ['concern_id', 'alternative_id'])

        # Adding model 'State'
        db.create_table('gridMng_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('gridMng', ['State'])

        # Adding model 'Facilitator'
        db.create_table('gridMng_facilitator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('gridMng', ['Facilitator'])

        # Adding model 'Session'
        db.create_table('gridMng_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('facilitator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Facilitator'])),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.State'])),
            ('invitationKey', self.gf('django.db.models.fields.TextField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('gridMng', ['Session'])

        # Adding model 'SessionIterationState'
        db.create_table('gridMng_sessioniterationstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Session'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.State'])),
        ))
        db.send_create_signal('gridMng', ['SessionIterationState'])

        # Adding unique constraint on 'SessionIterationState', fields ['iteration', 'session']
        db.create_unique('gridMng_sessioniterationstate', ['iteration', 'session_id'])

        # Adding model 'UserParticipateSession'
        db.create_table('gridMng_userparticipatesession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Session'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('gridMng', ['UserParticipateSession'])

        # Adding unique constraint on 'UserParticipateSession', fields ['session', 'user']
        db.create_unique('gridMng_userparticipatesession', ['session_id', 'user_id'])

        # Adding model 'SessionGrid'
        db.create_table('gridMng_sessiongrid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Session'])),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Grid'])),
        ))
        db.send_create_signal('gridMng', ['SessionGrid'])

        # Adding unique constraint on 'SessionGrid', fields ['iteration', 'session']
        db.create_unique('gridMng_sessiongrid', ['iteration', 'session_id'])

        # Adding model 'ResponseGrid'
        db.create_table('gridMng_responsegrid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Session'])),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gridMng.Grid'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('gridMng', ['ResponseGrid'])

        # Adding unique constraint on 'ResponseGrid', fields ['iteration', 'user', 'session']
        db.create_unique('gridMng_responsegrid', ['iteration', 'user_id', 'session_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ResponseGrid', fields ['iteration', 'user', 'session']
        db.delete_unique('gridMng_responsegrid', ['iteration', 'user_id', 'session_id'])

        # Removing unique constraint on 'SessionGrid', fields ['iteration', 'session']
        db.delete_unique('gridMng_sessiongrid', ['iteration', 'session_id'])

        # Removing unique constraint on 'UserParticipateSession', fields ['session', 'user']
        db.delete_unique('gridMng_userparticipatesession', ['session_id', 'user_id'])

        # Removing unique constraint on 'SessionIterationState', fields ['iteration', 'session']
        db.delete_unique('gridMng_sessioniterationstate', ['iteration', 'session_id'])

        # Removing unique constraint on 'Ratings', fields ['concern', 'alternative']
        db.delete_unique('gridMng_ratings', ['concern_id', 'alternative_id'])

        # Deleting model 'Grid'
        db.delete_table('gridMng_grid')

        # Deleting model 'Alternatives'
        db.delete_table('gridMng_alternatives')

        # Deleting model 'Concerns'
        db.delete_table('gridMng_concerns')

        # Deleting model 'Ratings'
        db.delete_table('gridMng_ratings')

        # Deleting model 'State'
        db.delete_table('gridMng_state')

        # Deleting model 'Facilitator'
        db.delete_table('gridMng_facilitator')

        # Deleting model 'Session'
        db.delete_table('gridMng_session')

        # Deleting model 'SessionIterationState'
        db.delete_table('gridMng_sessioniterationstate')

        # Deleting model 'UserParticipateSession'
        db.delete_table('gridMng_userparticipatesession')

        # Deleting model 'SessionGrid'
        db.delete_table('gridMng_sessiongrid')

        # Deleting model 'ResponseGrid'
        db.delete_table('gridMng_responsegrid')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gridMng.alternatives': {
            'Meta': {'ordering': "['id']", 'object_name': 'Alternatives'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Grid']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gridMng.concerns': {
            'Meta': {'ordering': "['id']", 'object_name': 'Concerns'},
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Grid']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leftPole': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'rightPole': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'gridMng.facilitator': {
            'Meta': {'ordering': "['id']", 'object_name': 'Facilitator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'gridMng.grid': {
            'Meta': {'ordering': "['id']", 'object_name': 'Grid'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 1, 0, 0)', 'null': 'True'}),
            'dendogram': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'grid_type': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'usid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'gridMng.ratings': {
            'Meta': {'unique_together': "(('concern', 'alternative'),)", 'object_name': 'Ratings'},
            'alternative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Alternatives']"}),
            'concern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Concerns']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'gridMng.responsegrid': {
            'Meta': {'ordering': "['id']", 'unique_together': "(('iteration', 'user', 'session'),)", 'object_name': 'ResponseGrid'},
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Grid']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Session']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'gridMng.session': {
            'Meta': {'ordering': "['id']", 'object_name': 'Session'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'facilitator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Facilitator']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitationKey': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.State']"}),
            'usid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'gridMng.sessiongrid': {
            'Meta': {'ordering': "['id']", 'unique_together': "(('iteration', 'session'),)", 'object_name': 'SessionGrid'},
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Grid']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Session']"})
        },
        'gridMng.sessioniterationstate': {
            'Meta': {'ordering': "['id']", 'unique_together': "(('iteration', 'session'),)", 'object_name': 'SessionIterationState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Session']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.State']"})
        },
        'gridMng.state': {
            'Meta': {'ordering': "['id']", 'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'gridMng.userparticipatesession': {
            'Meta': {'ordering': "['id']", 'unique_together': "(('session', 'user'),)", 'object_name': 'UserParticipateSession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gridMng.Session']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['gridMng']