# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'standbase_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datechanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'standbase', ['Topic'])

        # Deleting field 'StandSession.venueid'
        db.delete_column(u'standbase_standsession', 'venueid')

        # Deleting field 'StandSession.message'
        db.delete_column(u'standbase_standsession', 'message')

        # Deleting field 'StandSession.message_slug'
        db.delete_column(u'standbase_standsession', 'message_slug')

        # Adding field 'StandSession.topic'
        db.add_column(u'standbase_standsession', 'topic',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['standbase.Topic'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table(u'standbase_topic')

        # Adding field 'StandSession.venueid'
        db.add_column(u'standbase_standsession', 'venueid',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'StandSession.message'
        db.add_column(u'standbase_standsession', 'message',
                      self.gf('django.db.models.fields.CharField')(default='something', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'StandSession.message_slug'
        db.add_column(u'standbase_standsession', 'message_slug',
                      self.gf('django.db.models.fields.CharField')(default='something', max_length=255, blank=True),
                      keep_default=False)

        # Deleting field 'StandSession.topic'
        db.delete_column(u'standbase_standsession', 'topic_id')


    models = {
        u'standbase.standsession': {
            'Meta': {'object_name': 'StandSession'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datefinished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datelive': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geocode': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'t5k6ufmdqmab2sviogimo9lmwzk5dxp9nhi81dnzuqjcw2icz5'", 'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['standbase.Topic']", 'null': 'True', 'blank': 'True'}),
            'vendorid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'standbase.topic': {
            'Meta': {'object_name': 'Topic'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['standbase']