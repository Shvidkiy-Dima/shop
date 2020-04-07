from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from .models import PayRecord
from shop.apps.order.models import OrderModel
from .utils import send_mail_to_client
import logging
import stripe

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SERCRET_KEY
O_I = settings.ORDER_SESSION_ID

@method_decorator(csrf_exempt, name='dispatch')
class PaymentResult(TemplateView):
    template_name = None


class StripePay(View):

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(OrderModel, id=request.session.get(O_I))
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(order.total_price * 100),
            currency='usd',
            description=''
        )
        order.make_sales()
        PayRecord.objects.create(client=order.get_full_name(), payment_system='stripe', price=order.total_price)
        send_mail_to_client(order)
        logger.info('Payment Completed. Order №%s' % order.id)
        return redirect('payment:done')




