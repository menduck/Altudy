from django import forms
from .models import Study, Announcement
from taggit.forms import TagWidget, TagField

from reviews.fields import SpaceSeparatedTagsField

class StudyForm(forms.ModelForm):    
    class Meta:
        model = Study
        fields = (
            'title', 
            'description',
            'language',
            'category',
            'capacity',
            'start_date',
            'end_date',
            'days',
            'start_time',
            'end_time',
            'join_condition',
            )
        labels = {
            # 'title': '', 
            # 'description': '',
            # 'language': '',
            # 'category': '',
            # 'capacity': '스터디 최대 인원수',
            # 'start_date': '스터디 시작일',
            # 'end_date': '스터디 종료일',
            # 'days': '스터디 진행 요일',
            # 'start_time': '스터디 시작시간',
            # 'end_time': '스터디 종료시간',
            # 'join_condition': '가입 요청 여부',
            }
        widgets = {
            'title': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={}),
            'language': forms.SelectMultiple(attrs={}),
            'category': TagWidget(attrs={}),
            'capacity': forms.NumberInput(attrs={}),
            'start_date': forms.DateInput(attrs={'type':'date',}),
            'end_date': forms.DateInput(attrs={'type':'date',}),
            'days': forms.SelectMultiple(attrs={}),
            'start_time': forms.TimeInput(attrs={'type':'time',}),
            'end_time': forms.TimeInput(attrs={'type':'time',}),
            'join_condition': forms.Select(attrs={}),
        }
        help_texts = {
            'category': '태그를 입력하세요. 공백문자로 태그를 구분하며 대소문자를 구분하지 않습니다.',
            'capacity': '최대 인원 수는 10명입니다.',
        }
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)