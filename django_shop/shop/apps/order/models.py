from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils import timezone

from shop.apps.core.model_mixins import BaseShopMixin, CurrencyBaseShopMixin
from shop.apps.core.models import Variant

import logging

logger = logging.getLogger(__name__)



class Shipping(CurrencyBaseShopMixin):
    name = models.CharField(max_length=124)
    price = models.IntegerField()
    contact = models.CharField(max_length=124)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Службы доставки')

class OrderModel(CurrencyBaseShopMixin):

    first_name = models.CharField(_('Имя заказчика'), max_length=64)
    last_name = models.CharField(_('Фамилия заказчика'), max_length=64)
    address = models.CharField(_('Адресс заказчика'), max_length=200)
    country = models.CharField(_('Страна'), max_length=200)
    city = models.CharField(_('Город заказчика'), max_length=100)
    postal_code = models.CharField(_('Почтовый код'), max_length=100)
    paid = models.BooleanField(_('Оплачено'), default=False)
    total_price = models.FloatField(_('Итоговая цена'), default=0)
    email = models.EmailField('Email', max_length=124)
    taxes = models.FloatField(default=0)
    shipping = models.ForeignKey(Shipping, verbose_name=_('Способ доставки'), on_delete=models.SET_NULL,
                                        null=True)

    def make_sales(self):
        for item in self.orderitem_set.all().select_related('variant_product'):
            item.variant_product.sales += item.count
            item.variant_product.count -= item.count
            item.variant_product.last_sale = timezone.now()
            item.variant_product.save(update_fields=['sales', 'count', 'last_sale'])
            logger.info('Sales product %s variant %s: sales + %s, count - %s: sales %s, count %s' %
                        (item.type_product, item.variant_product, item.count, item.count,
                         item.variant_product.sales, item.variant_product.count))
        self.paid = True
        self.save(update_fields=['paid'])


    def set_ship_price(self):
        self.total_price += self.shipping.price


    def set_taxes_price(self):
        # compute taxes
        self.total_price += self.taxes

    def get_full_address(self):
        return '%s, %s, %s, %s' % (self.country, self.city, self.address, self.postal_code)

    def set_items(self, cart):
        for variant, count, exceed in cart.get_items():
            if not exceed:
                price = variant.price * count
                OrderItem.objects.create(count=count, variant_product=variant, price=price, order=self)
                self.total_price += price
        self.set_ship_price()
        self.set_taxes_price()
        self.save(update_fields=['total_price'])



    def get_absolute_url(self):
        return reverse('order:order-pay-page')

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['-date_create']
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return "Заказ № %d" % self.id

class OrderItem(BaseShopMixin):
    count = models.IntegerField(_('Кол-во единиц товара'), default=1)
    variant_product = models.ForeignKey(Variant, verbose_name=_('Тип товара'), on_delete=models.PROTECT)
    price = models.FloatField(_('Цена'))
    order = models.ForeignKey(OrderModel, verbose_name=_("Ссылка на заказ"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def type_product(self):
        return self.variant_product.product

    class Meta:
        ordering = ['-price']
        verbose_name = _('Единица заказа')
        verbose_name_plural = _('Единицы заказа')


