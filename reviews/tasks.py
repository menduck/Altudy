from celery import shared_task

@shared_task
def remove_unused_tags(obj):
    for tag in obj.tags.prefetch_related('problem_set', 'review_set', 'comment_set'):
        if tag.problem_set.count() == tag.review_set.count() == tag.comment_set.count() == 0:
            tag.delete()