from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import PayRecord
from shop.apps.order.models import OrderModel
from .utils import send_mail_to_client

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import logging

logger = logging.getLogger(__name__)

@receiver(valid_ipn_received)
def done_paypal(sender, **kwargs):
    # if sender.payment_status == ST_PP_COMPLETED:
    order = get_object_or_404(OrderModel, id=sender.invoice)
    order.make_sales()
    PayRecord.objects.create(client=order.get_full_name(), payment_system='paypal', price=order.total_price)
    send_mail_to_client(order)
    logger.info('Payment Completed. Order №%s' % order.id)

