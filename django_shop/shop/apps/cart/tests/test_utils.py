from django.test.testcases import TestCase

from shop.apps.core.models import Variant
from shop.apps.core.tests.main import ProductTestMixin
from ..utils import CartObj

from model_mommy import mommy

class CartTestMixin(ProductTestMixin):

    def create_cart(self, request, count_products=6, variants=6, count_variants=6, price=30):
        cart = CartObj(request)
        for i in range(count_products):
            product = self.create_product(price=price, variants=variants, count_variants=count_variants)
            for v in product.variant_set.all():
                for i in range(v.count):
                    cart.action('add', v.id)
        return cart



class TestCart(CartTestMixin, TestCase):
    variants = 6
    count_variants = 6
    price = 20
    count_products = 6

    def setUp(self):
        super().setUp()
        self.cart = self.create_cart(self.client,
                                     count_products=self.count_products,
                                     variants=self.variants,
                                     count_variants=self.count_variants, price=self.price)

    @property
    def initial_count(self):
        return self.count_variants * self.variants * self.count_products

    def test_count(self):
        """ Количество товаров в корзине """
        self.assertTrue(self.cart.count == self.initial_count, 'cart count error')

    def test_exceed(self):
        """
        Сумма всех товаров в которую не входит сумма последнего товара
        кол-во которого превышает кол-во единиц товара на складе
        """
        v, count, _ = next(self.cart.get_items())
        self.cart.action('add', v.id)
        exceed = v.price * count
        expected_price = self.price * self.initial_count - exceed
        cart_price = self.cart.total_price
        self.assertTrue(cart_price == expected_price, 'cart total price error: expected %s instead %s' %
                        (cart_price, expected_price))


    def test_add(self):
        v = mommy.make(Variant)
        self.cart.action('add', v.id)
        self.assertTrue(self.cart.count == (self.initial_count + 1))
        self.assertTrue(self.cart.count_order(v.id) == 1)

    def test_delete(self):
        v, _, _ = next(self.cart.get_items())
        count = self.cart.count_order(v.id)
        self.cart.action('delete', v.id)
        self.assertTrue(self.cart.count == (self.initial_count - 1))
        self.assertTrue(self.cart.count_order(v.id) == (count - 1))
        while self.cart.count_order(v.id) > 1:
            self.cart.action('delete', v.id)
        self.assertTrue(self.cart.count_order(v.id) == 1)
        self.cart.action('delete', v.id)
        self.assertFalse(self.cart.count_order(v.id) == 0)

    def test_delete_all(self):
        v, _, _ = next(self.cart.get_items())
        count = self.cart.count_order(v.id)
        all_price = v.price * count
        self.cart.action('delete_all', v.id)
        self.assertTrue(self.cart.count == (self.initial_count - count), 'delete_all: cart count error')
        expected_price = self.price * self.initial_count - all_price
        cart_price = self.cart.total_price
        self.assertTrue(cart_price == expected_price, 'cart total price error: expected %s instead %s' %
                        (cart_price, expected_price))

    def test_clear(self):
        self.cart.action('clear', None)
        self.assertTrue(self.cart.count == 0, 'clear: count')
        self.assertTrue(self.cart.total_price == 0, 'clear: total')
        self.assertTrue(self.cart.is_empty(), 'clear: is_empty')
        self.assertFalse(len(self.cart.orders), 'clear: len')



