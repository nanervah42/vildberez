from django import template
import datetime

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)

