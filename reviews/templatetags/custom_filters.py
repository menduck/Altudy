import pickle as pk
import markdown as md
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter('dir')
def get_attributes(obj):
    return dir(obj)


@register.filter('type')
def get_attributes(obj):
    return type(obj)


@register.filter
def markdown(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(md.markdown(value, extensions=extensions))


@register.filter
def pickle(obj):
    return pk.dumps(obj, 0)
