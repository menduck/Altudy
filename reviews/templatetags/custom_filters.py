import pickle as pk
import markdown as md
from cryptography.fernet import Fernet
from django import template
from django.utils.safestring import mark_safe


register = template.Library()
key = Fernet.generate_key()
fernet = Fernet(key)

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
    pickled = pk.dumps((obj.__class__.__name__, obj.pk), 0)
    return str(fernet.encrypt(pickled))[2:-1]


@register.filter('class')
def get_attributes(obj):
    '''returns class name'''
    return obj.__class__.__name__