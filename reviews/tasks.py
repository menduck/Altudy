from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.db.models import Count
from taggit.models import Tag

@shared_task
def remove_unused_tags():
    Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
