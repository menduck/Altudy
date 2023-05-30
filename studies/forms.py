from django import forms
from .models import Study, Announcement
from taggit.forms import TagWidget

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ('title', 'description', 'language', 'category', 'capacity', 'start_date', 'end_date',)
        widgets = {
            'title': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={}),
            'language': forms.SelectMultiple(attrs={}),
            'category': TagWidget(attrs={}),
            'capacity': forms.NumberInput(attrs={}),
            'start_date': forms.DateInput(attrs={}),
            'end_date': forms.DateInput(attrs={}),
        }
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)