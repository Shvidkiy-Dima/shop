from django.template.loader import render_to_string
from django.conf import settings

from shop.apps.core.tasks import sendler_email

PDF_TEMPLATE = 'order/pdf-templates/order-pdf.html'

def send_mail_to_client(order):
    client_email = order.email
    html = render_to_string(PDF_TEMPLATE, {'order': order})
    sendler_email.delay('Заказ №%s оплачен' % order.id,
                        'Дорогой, %s, вы успешно сделали заказ. Номер вашего заказа %s' % (
                            order.first_name, order.id),
                        settings.DEFAULT_FROM_EMAIL, [client_email], pdf_data=html)