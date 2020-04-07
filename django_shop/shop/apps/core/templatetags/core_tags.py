from django import template
from django.conf import settings

from shop.apps.order.models import OrderModel
from shop.apps.core.utils import get_or_none

import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('core/tags/navbar.html')
def navbar(**kwargs):
    return kwargs


@register.inclusion_tag('core/tags/main_filter.html')
def main_filter(**kwargs):
    return kwargs


@register.simple_tag
def get_settings(conf):
    return getattr(settings, conf)

@register.inclusion_tag('core/tags/continue_order.html')
def continue_order(request):
    data = request.session.get(settings.ORDER_SESSION_ID)
    if data:
        data = get_or_none(OrderModel, {'id': data})
        if data and data.paid:
            del request.session[settings.ORDER_SESSION_ID]
            logger.info('Cookie order %s was deleted' % data.id)
            data = None
    return {'continue': data}

