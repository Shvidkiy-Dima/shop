from django.test import TestCase

from .main import ProductTestMixin
from shop.apps.core.models import Product
from shop.apps.core.utils import get_or_none

class UtilsTest(ProductTestMixin, TestCase):

    def test_get_or_none(self):
        self.assertTrue(get_or_none(Product, {'id': 1}) is None)
        product = self.create_product()
        self.assertTrue(get_or_none(Product, {'id': 1}).id == product.id)

