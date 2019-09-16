from django import template

register = template.Library()


@register.filter(name='lookup_rounding_method')
def lookup_rounding_method(value):
    CHOICES = {
        1: "切落し(浮き切捨て、沈み切上げ)",
        2: "四捨五入",
        3: "五捨六入",
    }
    try:
        return CHOICES[value]
    except KeyError:
        return value


@register.filter(name='lookup_uma_method')
def lookup_uma_method(value):
    CHOICES = {
        "A1": "5-10",
        "A2": "10-20",
        "A3": "10-30",
        "B1": "マルA式",
    }
    try:
        return CHOICES[value]
    except KeyError:
        return value


