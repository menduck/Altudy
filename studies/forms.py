from django import forms
from .models import Study, Announcement


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ('title', 'description', 'language', 'category', 'capacity', 'start_date', 'end_date',)
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)