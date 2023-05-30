from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField

# Create your models here.
LANGUAGE_CHOICES = [
    ('py', 'Python'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('c', 'C'),
    ('c++', 'C++'),
    ('c#', 'C#'),
    ('ruby', 'Ruby'),
    ('dart', 'Dart'),
    ('scala', 'Scala'),
    ('go', 'Golang'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('node_js', 'Node.js'),
]


class Study(models.Model):
    # 스터디장 유저
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    # 스터디 주 언어
    language = MultiSelectField(choices=LANGUAGE_CHOICES)
    category = TaggableManager(blank=True)
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