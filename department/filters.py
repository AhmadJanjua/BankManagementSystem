import re

from django import template

register = template.Library()

@register.filter
def findall(value, pattern):
    matches = re.findall(pattern, value)
    return matches