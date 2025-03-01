from django import template
from ..models import Brand, Color

register = template.Library()

@register.simple_tag
def get_brands():
    return Brand.objects.all()

@register.simple_tag
def get_colors():
    return Color.objects.all()
