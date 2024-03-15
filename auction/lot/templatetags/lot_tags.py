from django.utils.safestring import mark_safe
from django import template
import markdown
import os
from django.conf import settings


register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
 return mark_safe(markdown.markdown(text))