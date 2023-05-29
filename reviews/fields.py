from django import forms
from taggit.utils import parse_tags


class SpaceSeparatedTagsField(forms.CharField):
    def clean(self, value):
        '''
        space separates tags
        '''
        tags = parse_tags(value)
        return super().clean(tags)
