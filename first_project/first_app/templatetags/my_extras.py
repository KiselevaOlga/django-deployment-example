from urllib.parse import quote_plus
from django import template

register=template.Library()

@register.filter(name="adds")
def adds(value, arg):
    value = value+arg
    return value