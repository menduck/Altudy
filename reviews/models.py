# from celery import shared_task
from django.conf import settings
from django.db import models
# from django.urls import reverse_lazy
from taggit.managers import TaggableManager


# Create your models here.
class Problem(models.Model):
    title = models.CharField('제목', max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='게시자', on_delete=models.CASCADE)
    
    # url shortener + 미리보기 + Validator
    url = models.CharField('문제 링크', max_length=1000)
    tags = TaggableManager(blank=True)
    description = models.TextField('설명')

    class Meta:
        db_table = 'problem'


    def __str__(self) -> str:
        return self.title

    # def get_absolute_url(self):
    #     return reverse_lazy('reviews:detail', kwargs={'pk': self.pk})

    # @shared_task
    # def remove_unused_tags(self):
    #     for tag in self.tags.prefetch_related('problem_set', 'review_set', 'comment_set'):
    #         if tag.problem_set.count() == tag.review_set.count() == tag.comment_set.count() == 0:
    #             tag.delete()


class Review(models.Model):
    content = models.TextField('내용')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.CASCADE)
    problem = models.ForeignKey("reviews.Problem", verbose_name='문제', on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'review'


    def __str__(self) -> str:
        return f'Review by {self.user}, on {self.problem}'


class Comment(models.Model):
    content = models.TextField('내용')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.CASCADE)
    review = models.ForeignKey("reviews.Review", verbose_name='리뷰', on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'comment'

    def __str__(self) -> str:
        return f'Comment by {self.user}, on {self.review}'
