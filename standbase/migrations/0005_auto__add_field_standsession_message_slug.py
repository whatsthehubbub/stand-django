# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StandSession.message_slug'
        db.add_column(u'standbase_standsession', 'message_slug',
                      self.gf('django.db.models.fields.CharField')(default='something', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StandSession.message_slug'
        db.delete_column(u'standbase_standsession', 'message_slug')


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
            'message_slug': ('django.db.models.fields.CharField', [], {'default': "'something'", 'max_length': '255', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'4ujvhpa4on9ombjfgdf4z0x7lwaq62sr3025zuc4me66t8jt2g'", 'max_length': '255'}),
            'vendorid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venueid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['standbase']