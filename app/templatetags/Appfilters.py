from django import template

register = template.Library()

FORBIDDEN_WORDS = ['отрасль', 'области', 'граждане', 'автомобили']

@register.filter()
def censor(text):
    """Фильтр применен в шаблоне post"""

    for i in FORBIDDEN_WORDS:
        if i in text:
            num = text.find(i)
            _find = text[num:num + len(i)]

            text = text.replace(_find, text[num] + '*' * (len(_find) - 1) + '!')

    return text

@register.filter()
def create_name(text):
    if text == None or '':
        return ''
    else:
        return f'{text[:text.find("@")]}'

@register.filter()
def rpfl(text):
    '''replace first and last letter
        Применен в шаблоне posts '''

    temp = text.split()
    for num, var in enumerate(temp):
        if var in FORBIDDEN_WORDS:
            temp[num] = f'*{var[1:len(var) - 1]}*'

    return ' '.join(temp)