from django import forms
from .models import Study, Announcement
from taggit.forms import TagWidget

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
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)