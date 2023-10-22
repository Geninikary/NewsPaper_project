from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': '₽',
    'usd': '$'
}

@register.filter()
def currency(value, code='rub'):
    """ valiue: знвчение, к кторому нужно применить фильтр"""

    postfix = CURRENCIES_SYMBOLS[code]

    return f'{value} {postfix} '
