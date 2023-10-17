from django import template

register = template.Library()

WORD_UNDER_CENSORSHIP = ['город', 'закрыть', 'произведение']


@register.filter()
def censor(value):
    value_split = value.split()
    if type(value) is not str:
        raise ValueError('Фильтрация невозможна, требуется переменные str типа')
    for word in WORD_UNDER_CENSORSHIP:
        if word in value_split:
            censor_word = word[0] + '*' * (len(word)-1)
            value = value.replace(word, censor_word)

    return value
