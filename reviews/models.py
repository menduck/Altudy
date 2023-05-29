from django.conf import settings
from django.db import models


# Create your models here.
class Problem(models.Model):
    title = models.CharField('제목', max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='게시자', on_delete=models.CASCADE)
    url = models.CharField('문제 링크', max_length=1000)

    def __str__(self) -> str:
        return self.title


class Solution(models.Model):
    content = models.TextField('내용')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.CASCADE)
    problem = models.ForeignKey("reviews.Problem", verbose_name='리뷰', on_delete=models.CASCADE)
    # language, category, tag

    def __str__(self) -> str:
        return f'Solution by {self.user}, on {self.problem}'


class Comment(models.Model):
    content = models.TextField('내용')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.CASCADE)
    solution = models.ForeignKey("reviews.Solution", verbose_name='리뷰', on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')

    def __str__(self) -> str:
        return f'Comment by {self.user}, on {self.solution}'


class Tag(models.Model):
    pass