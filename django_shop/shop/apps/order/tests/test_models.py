from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy


from shop.apps.order.models import Shipping, OrderModel
from shop.apps.cart.tests.test_utils import CartTestMixin




class OrderModelTest(CartTestMixin, TestCase):
    count_products = 6
    variants = 6
    count_variants = 6
    price = 30

    def setUp(self):
        super().setUp()
        shipping = mommy.make(Shipping)
        self.order = mommy.make(OrderModel, shipping=shipping)

    def get_cart(self, count_products, variants, count_variants, price):
        """
        Заполнил корзину товарами
        """
        return self.create_cart(request=self.client, count_products=count_products,
                                variants=variants, count_variants=count_variants,
                                price=price)


    def test_set_items(self):
        cart = self.get_cart(self.count_products, self.variants, self.count_variants, self.price)
        self.order.set_items(cart)

        total = (self.count_products * self.variants * self.count_variants * self.price) \
                + self.order.shipping.price + self.order.taxes
        """
        (count_products * variants * count_variants) = Общее кол-во, и у всех одинаковая цена
        """
        self.assertTrue(self.order.total_price == total)

        items = self.order.orderitem_set.all()

        self.assertTrue(items.count() == (self.count_products * self.variants))
        self.assertTrue(sum(
            c.count for c in items) == (self.count_products * self.variants * self.count_variants))


    def test_full_address(self):
        self.assertTrue(self.order.get_full_address() == '%s, %s, %s, %s' %
                        (self.order.country, self.order.city, self.order.address, self.order.postal_code))

    def test_full_name(self):
        self.assertTrue(self.order.get_full_name() == '%s %s' % (self.order.first_name ,self.order.last_name))

    def test_absolute_url(self):
        self.assertTrue(self.order.get_absolute_url() == reverse('order:order-pay-page'))


    def test_make_sales(self):
        cart = self.get_cart(self.count_products, self.variants, self.count_variants, self.price)
        self.order.set_items(cart)
        items = self.order.orderitem_set.all()

        """
        Высчитал остаток ед-товара и кол-во продаж
        """

        self.order.make_sales()

        for i in items.all().select_related('variant_product'):
            self.assertTrue(i.variant_product.sales == i.count)
            self.assertTrue(i.variant_product.count == 0)

