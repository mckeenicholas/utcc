from django import template

register = template.Library()


@register.filter
def format_centiseconds(value):
    if value is None:
        return ""

    minutes = value // 6000
    remaining = value % 6000
    seconds = remaining // 100
    cents = remaining % 100

    if minutes > 0:
        return f"{minutes}:{seconds:02d}.{cents:02d}"
    return f"{seconds}.{cents:02d}"
