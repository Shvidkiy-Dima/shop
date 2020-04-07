from django import template

from shop.apps.design.models import Slides
from shop.apps.core.models import Product
from shop.apps.core.utils import get_or_none

register = template.Library()



@register.inclusion_tag('design/main-slides.html')
def slides():
    slides = Slides.objects.all()
    if slides:
        main, slides = slides[0], slides[1:]
        indicator = range(1, len(slides)+1)
        return {'slides': slides, 'main': main, 'indicator': indicator, 'w': True}



@register.inclusion_tag('design/main-slides.html')
def slides_products(id, size='500px'):
    p = get_or_none(Product, {'id': id})
    if p:
        main, *slides = p.image, p.image2, p.image3
        indicator = range(1, len(slides)+1)
        return {'slides': slides, 'main': main, 'size': size, 'indicator': indicator}