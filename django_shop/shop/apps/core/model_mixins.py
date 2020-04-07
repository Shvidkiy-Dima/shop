from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings

from .utils import my_slugify



class BaseShopMixin(models.Model):
    date_create = models.DateTimeField(_('Дата создания'), default=timezone.now)

    def get_date_create(self):
        return self.date_create.strftime(settings.ADMIN_DATE_FORMAT)
    get_date_create.short_description = 'Дата создания'

    class Meta:
        abstract = True

class CurrencyBaseShopMixin(BaseShopMixin):
    CURRENCIES = (('USD', '$'),)
    currency = models.CharField(max_length=10, choices=CURRENCIES, default='USD')

    @property
    def c(self):
        return self.get_currency_display()


    class Meta:
        abstract = True



class ShopMixin(BaseShopMixin):

    stat = (('A', 'Active'),
            ('D', 'Deactive'))

    date_update = models.DateTimeField(_('Дата последнего изменения'), default=timezone.now)
    image = models.ImageField(upload_to='shop_media/', blank=True, null=True)
    status = models.CharField(choices=stat, max_length=20, default='A')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, max_length=65)
    name = models.CharField(max_length=124, unique=True)



    def save(self, *args, **kwargs):
        self.slug = my_slugify(self.name)
        super().save()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True




