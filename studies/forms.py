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
            )
        labels = {
            # 'title': '', 
            # 'description': '',
            # 'language': '',
            # 'category': '',
            # 'capacity': '',
            # 'start_date': '',
            # 'end_date': '',
            # 'days': '',
            # 'start_time': '',
            # 'end_time': '',
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
        }
        help_texts = {
            'category': '태그를 입력하세요. 공백문자로 태그를 구분하며 대소문자를 구분하지 않습니다.',
        }
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)