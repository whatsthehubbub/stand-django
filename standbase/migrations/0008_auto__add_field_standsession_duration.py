# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StandSession.duration'
        db.add_column(u'standbase_standsession', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StandSession.duration'
        db.delete_column(u'standbase_standsession', 'duration')


    models = {
        u'standbase.standsession': {
            'Meta': {'object_name': 'StandSession'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datefinished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datelive': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'geocode': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'s20itwy1avlx39plh5u8mecburz54vi5wtchw3kq1cy5tegxvx'", 'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['standbase.Topic']", 'null': 'True', 'blank': 'True'}),
            'vendorid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'standbase.topic': {
            'Meta': {'object_name': 'Topic'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['standbase']