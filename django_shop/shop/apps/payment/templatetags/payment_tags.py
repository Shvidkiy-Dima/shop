from django import template
from django.conf import settings
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm


register = template.Library()

@register.inclusion_tag('payment/paypal.html')
def paypal(request, order):
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_price,
        'item_name': 'Заказ %d' % order.id,
        'invoice': str(order.id),
        'currency_code': settings.CUR_CURRENCY_COD,
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:cancel'))
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return {'form': form}

@register.inclusion_tag('payment/stripe.html')
def stripe(order):
    key = settings.STRIPE_PUBLISHABLE_KEY
    amount, full_amount = order.total_price, int(order.total_price * 100)
    return {'key': key, 'amount': amount, 'full_amount': full_amount}
