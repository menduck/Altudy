from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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

STUDY_DAYS = [
    ('월', '월요일'),
    ('화', '화요일'),
    ('수', '수요일'),
    ('목', '목요일'),
    ('금', '금요일'),
    ('토', '토요일'),
    ('일', '일요일'),
]

class Study(models.Model):
    # 스터디장 유저
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lead_studies')
    
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    # 스터디 주 언어
    language = MultiSelectField(choices=LANGUAGE_CHOICES, blank=True)
    category = TaggableManager(blank=True)
    # 스터디 최대 인원수
    capacity = models.PositiveSmallIntegerField(default=5, validators=[
        MaxValueValidator(10),
        MinValueValidator(2),
    ])
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # 스터디 진행 요일
    days = MultiSelectField(choices=STUDY_DAYS, blank=True)
    # 스터디 진행 시작, 끝 시간
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    join_condition = models.PositiveSmallIntegerField(choices=[(1, '승인 필요'), (2, '바로 가입')], default=1)
    # 스터디 가입 요청
    join_request = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='study_request', blank=True)
    
    # 스터디 참여중인 user, 중개테이블 - Studying
    studying_users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='user_studies', through='Studying', blank=True)

    post_index = models.IntegerField('게시글 번호', default=1)
    
    def __str__(self) -> str:
        return self.title
    
    
# study - user M:N 중개 테이블
class Studying(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    
    permission = models.PositiveSmallIntegerField(default=1)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    
class Announcement(models.Model):
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE, related_name='announcements')
    
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