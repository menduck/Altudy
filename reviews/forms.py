from django import forms
from taggit.forms import TagWidget

from .fields import SpaceSeparatedTagsField
from .models import Problem
    

class ProblemForm(forms.ModelForm):
    tags = SpaceSeparatedTagsField(widget=TagWidget(), required=True)
    class Meta:
        model = Problem
        fields = (
            'title',
            'url',
            'tags',
        )
