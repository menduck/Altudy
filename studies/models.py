from django.db import models
from django.conf import settings

# Create your models here.
# 스터디 언어
class Language(models.Model):
    language = models.CharField(max_length=10)


# 스터디 성향 카테고리
class Category(models.Model):
    content = models.CharField(max_length=10)
    
    
class Study(models.Model):
    # 스터디장 유저
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 스터디 주 언어
    language = models.ManyToManyField(to=Language, related_name='language_studies', blank=True)
    category = models.ManyToManyField(to=Category, related_name='category_studies', blank=True)
    
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    # 스터디 최대 인원수
    capacity = models.PositiveSmallIntegerField(default=5)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
# study - user M:N 중개 테이블
class Studying(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    
    permission = models.PositiveSmallIntegerField(default=1)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    
class Announcement(models.Model):
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 라이브 스터디방(?) 테이블
# class Attendance(models.Model):
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     class = models.ForeignKey(to=, on_delete=models.CASCADE)
    
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)