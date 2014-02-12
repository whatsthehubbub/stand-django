# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StandSession.secret'
        db.add_column(u'standbase_standsession', 'secret',
                      self.gf('django.db.models.fields.CharField')(default='95d(%-u^n(f2qmg!^ad1!duz6mue2tzu@a*d28!mvrtu&ox-%x', max_length=255),
                      keep_default=False)

        # Adding field 'StandSession.datefinished'
        db.add_column(u'standbase_standsession', 'datefinished',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StandSession.secret'
        db.delete_column(u'standbase_standsession', 'secret')

        # Deleting field 'StandSession.datefinished'
        db.delete_column(u'standbase_standsession', 'datefinished')


    models = {
        u'standbase.standsession': {
            'Meta': {'object_name': 'StandSession'},
            'datechanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datefinished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'u2k@alox%y99r8#5c1mk))klgil+*d013+m%g2fil$$fuu9xx$'", 'max_length': '255'}),
            'vendorid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venueid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['standbase']