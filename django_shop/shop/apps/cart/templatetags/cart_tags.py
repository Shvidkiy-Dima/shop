from django import template

from shop.apps.cart.utils import CartObj

register = template.Library()


@register.simple_tag
def count_products_cart(request):
    cart = CartObj(request)
    return cart.count

