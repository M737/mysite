from django import template

register = template.Library()

@register.simple_tag
def word_pronunciation(word, en):
    url = "https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan={}&text={}&spd=2&source=alading".format(en, word)
    print(url)
    return url