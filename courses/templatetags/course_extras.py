from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Check if a string ends with a given suffix"""
    return str(value).endswith(str(arg))

@register.filter
def startswith(value, arg):
    """Check if a string starts with a given prefix"""
    return str(value).startswith(str(arg))

