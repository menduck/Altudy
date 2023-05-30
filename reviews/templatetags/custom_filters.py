from django import template

register = template.Library()

@register.filter('dir')
def get_attributes(obj):
    return dir(obj)

@register.filter('type')
def get_attributes(obj):
    return type(obj)