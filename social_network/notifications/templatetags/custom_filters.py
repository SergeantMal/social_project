from django import template
from django.utils import timezone
from django.utils.timesince import timesince
import re
import locale

register = template.Library()

MONTH_NAMES = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}


@register.filter
def russian_date(value):
    if not value:
        return ''

    day = value.day
    month = MONTH_NAMES[value.month]
    year = value.year
    time = value.strftime('%H:%M')

    return f"{day} {month} {year} {time}"

@register.filter
def russian_timesince(value):
    if not value:
        return ''

    now = timezone.now()
    try:
        difference = now - value
    except:
        return value

    if difference.days == 0:
        if difference.seconds < 60:
            return 'только что'
        elif difference.seconds < 3600:
            minutes = difference.seconds // 60
            return f'{minutes} минут назад'
        else:
            hours = difference.seconds // 3600
            return f'{hours} часов назад'
    else:
        if difference.days == 1:
            return 'вчера'
        elif difference.days < 5:
            return f'{difference.days} дня назад'
        else:
            return f'{difference.days} дней назад'