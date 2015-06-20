from django import template


register = template.Library()

@register.filter
def encode_url(cooked_url):
    return cooked_url.replace(' ', '_')