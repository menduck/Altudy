from django import forms
from django_tuieditor.widgets import MarkdownEditorWidget
from django_tuieditor.fields import MarkdownFormField
from taggit.forms import TagWidget

from .fields import SpaceSeparatedTagsField
from .models import Problem, Review
    

class ProblemForm(forms.ModelForm):
    tags = SpaceSeparatedTagsField(widget=TagWidget(), required=False)
    class Meta:
        model = Problem
        fields = (
            'title',
            'url',
            'tags',
            'description',
        )


class ReviewForm(forms.ModelForm):
    tags = SpaceSeparatedTagsField(widget=TagWidget(), required=False)
    content = MarkdownFormField(
        label='내용',
        widget=MarkdownEditorWidget(),
    )
    class Meta:
        model = Review
        fields = (
            'tags',
            'content',
        )
