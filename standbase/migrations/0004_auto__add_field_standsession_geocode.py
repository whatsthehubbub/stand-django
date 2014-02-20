# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StandSession.geocode'
        db.add_column(u'standbase_standsession', 'geocode',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StandSession.geocode'
        db.delete_column(u'standbase_standsession', 'geocode')


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
            'message': ('django.db.models.fields.CharField', [], {'default': "'something'", 'max_length': '255', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'nq6pq6po5wnj8ffrarln216s3zifbnzbidmlc94yuq0wxacqw2'", 'max_length': '255'}),
            'vendorid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venueid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['standbase']