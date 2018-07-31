
from django import template

register = template.Library()

@register.simple_tag
def replace(path):
    return  path.replace('static','media')