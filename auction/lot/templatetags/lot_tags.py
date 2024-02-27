from django.utils.safestring import mark_safe
from django import template
import markdown
import os
from django.conf import settings


register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
 return mark_safe(markdown.markdown(text))

@register.simple_tag
def image_with_default(image_url):
    default_image_path = 'client/images/user/user.png'  # Set default image path here
    if image_url and os.path.exists(os.path.join(settings.MEDIA_ROOT, image_url)):
        return image_url
    else:
        return default_image_path