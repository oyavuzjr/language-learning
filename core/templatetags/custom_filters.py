# templatetags/custom_filters.py

import re
from django import template

register = template.Library()

@register.filter
def split_regex(value, pattern):
    return re.split(pattern, value)

@register.filter
def contains_underscore(value):
    return '_' in value
