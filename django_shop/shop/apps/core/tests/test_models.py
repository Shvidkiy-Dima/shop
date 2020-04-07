from django.test import TestCase
from django.urls import reverse

from .main import ProductTestMixin

class ProductTest(ProductTestMixin, TestCase):
    price = 40
    variants = 6
    count_variants = 6
    sales = 5

    def setUp(self):
        self.product = self.create_product(price=self.price,
                                           variants=self.variants,
                                           count_variants=self.count_variants,
                                           sales=self.sales)

    def test_get_count(self):
        count = self.variants * self.count_variants
        self.assertTrue(self.product.get_count() == count)

    def test_get_main_variant(self):
        self.assertTrue(self.product.get_main_variant == self.product.variant_set.first())

    def test_get_sales(self):
        sales = self.variants * self.sales
        self.assertTrue(self.product.get_sales() == sales)

    def test_absolute_url(self):
        url = reverse('core:detail-product-main', kwargs={'slug': self.product.slug})
        self.assertTrue(self.product.get_absolute_url() == url)