from django import template

register = template.Library()

@register.filter
def abs_value(value):
    """Return the absolute value of a number"""
    try:
        return abs(value)
    except (ValueError, TypeError):
        return value

@register.filter
def days_overdue(value):
    """Return the number of days overdue (positive number)"""
    if value < 0:
        return abs(value)
    return 0
