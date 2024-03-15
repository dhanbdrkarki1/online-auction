from django import template

register = template.Library()

@register.filter
def range_from_one_to(value):
    return range(1, value + 1)