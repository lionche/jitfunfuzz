from html import escape

from django.template.defaulttags import register
from django.utils.safestring import mark_safe, SafeData
from django.utils.text import normalize_newlines


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

