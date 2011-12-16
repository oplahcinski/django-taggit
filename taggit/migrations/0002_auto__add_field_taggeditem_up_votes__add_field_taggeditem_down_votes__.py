# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TaggedItem.up_votes'
        db.add_column('taggit_taggeditem', 'up_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'TaggedItem.down_votes'
        db.add_column('taggit_taggeditem', 'down_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'TaggedItem.score'
        db.add_column('taggit_taggeditem', 'score', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'TaggedItem.timestamp'
        db.add_column('taggit_taggeditem', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TaggedItem.up_votes'
        db.delete_column('taggit_taggeditem', 'up_votes')

        # Deleting field 'TaggedItem.down_votes'
        db.delete_column('taggit_taggeditem', 'down_votes')

        # Deleting field 'TaggedItem.score'
        db.delete_column('taggit_taggeditem', 'score')

        # Deleting field 'TaggedItem.timestamp'
        db.delete_column('taggit_taggeditem', 'timestamp')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'down_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'up_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['taggit']
