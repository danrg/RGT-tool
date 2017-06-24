from django import template
from ...settings import RECAPTCHA_PUBLIC_KEY

register = template.Library()


@register.simple_tag
def recaptcha_public_key():
    return RECAPTCHA_PUBLIC_KEY
