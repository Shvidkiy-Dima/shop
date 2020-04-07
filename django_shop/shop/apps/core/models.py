from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.urls import reverse

from .model_mixins import  ShopMixin, CurrencyBaseShopMixin




class Brand(ShopMixin):
    class Meta:
        verbose_name = _('Бренд')
        verbose_name_plural = _('Бренд')

class Category(ShopMixin):
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Variant(CurrencyBaseShopMixin):

    CHOISE_SIZE= (('S','S'),
                  ('M','M'),
                  ('L','L'),
                  ('XL','XL'),
                  ('2XL','2XL'),
                  ('3XL','3XL'),
                  ('4XL','4XL'),
                  ('5XL','5XL'))

    size = models.CharField(_('Размер товара'), max_length=5, choices=CHOISE_SIZE, null=True, blank=True)

    count = models.IntegerField(_('Кол-во единиц товара'), default=1)
    sales = models.IntegerField(_('Кол-во проданных единиц товара'), default=0)
    price = models.FloatField(_('Цена товара'))
    last_sale = models.DateTimeField(default=timezone.now)

    product = models.ForeignKey('Product', verbose_name=_('Товар'), on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' % (self.product.name, self.size or 'main')

    class Meta:
        ordering = ['-sales']

class Product(ShopMixin):

    features = models.CharField(_('Особенности товара'), max_length=524, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('Категория товара'), on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name=_('Бренд товара'), on_delete=models.CASCADE)
    average_price = models.FloatField(_('Средняя цена товара'), help_text=_('Для поиска'))
    image2 = models.ImageField(upload_to='shop_media/', blank=True, null=True)
    image3 = models.ImageField(upload_to='shop_media/', blank=True, null=True)


    def get_sales(self):
        return sum((i.sales for i in self.variant_set.all()))

    def get_count(self):
        return sum(v.count for v in self.variant_set.all())

    def get_absolute_url(self):
        return reverse('core:detail-product-main', kwargs={'slug': self.slug})

    @property
    def get_size(self):
        return self.variant_set.exclude(size=None)

    @property
    def get_main_variant(self):
        return self.variant_set.first()


    class Meta:
        ordering = ['-average_price']
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

