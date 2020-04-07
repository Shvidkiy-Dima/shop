from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'shop.apps.payment'

    def ready(self):
        import shop.apps.payment.signals