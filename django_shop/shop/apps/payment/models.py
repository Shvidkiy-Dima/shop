from django.db import models
from django.utils.translation import gettext as _
from shop.apps.core.model_mixins import CurrencyBaseShopMixin

class PayRecord(CurrencyBaseShopMixin):
    client = models.CharField(max_length=200)
    payment_system = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.client

    class Meta:
        ordering = ['-date_create']
        verbose_name = _('Запись оплаты')
        verbose_name_plural = _('Записи оплаты')
