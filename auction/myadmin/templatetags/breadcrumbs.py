# your_app/templatetags/breadcrumbs.py
from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def breadcrumbs(request):
    paths = []
    current_path = request.path_info.strip('/')

    print("current_path>>>>", current_path)
    previous_url = ''
    for path_part in current_path.split('/'):
        if path_part:
            paths.append({
                'url': f'{previous_url}/{path_part}/',
                'name': path_part.capitalize()
            })
            previous_url: paths[path_part.capitalize()]

    print(paths)

    return paths
