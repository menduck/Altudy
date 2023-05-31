import markdown
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter('dir')
def get_attributes(obj):
    return dir(obj)


@register.filter('type')
def get_attributes(obj):
    return type(obj)


@register.filter('markdown')
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))