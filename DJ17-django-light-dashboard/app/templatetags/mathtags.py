from django import template

register = template.Library()


@register.filter()
def percentof(t1, t2):
    try:
        return str(round((t1 / t2) * 100, 1))+'%'
    except (ZeroDivisionError, TypeError):
        return None
