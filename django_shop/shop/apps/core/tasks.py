from django.core.mail import EmailMessage
from django.http.response import HttpResponse

from weasyprint import HTML
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def sendler_email(subject, body, from_email, to_email, html_template=None, pdf_data=None, pdf_name='order.pdf'):
    email = EmailMessage(subject=subject, body=body, to=to_email,
                         from_email=from_email)
    if pdf_data:
        fileobj = HttpResponse()
        HTML(string=pdf_data).write_pdf(fileobj)
        email.attach(pdf_name, fileobj.content, 'application/pdf')
    try:
        email.send()
    except Exception as e:
        logger.error('Mail send error: %s' % e)
    else:
        logger.info('Message send!')