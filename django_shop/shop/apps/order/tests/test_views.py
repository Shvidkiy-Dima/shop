from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from shop.apps.order.models import OrderModel, Shipping
from shop.apps.core.tests.main import ProductTestMixin

from model_mommy import mommy


O_I = settings.ORDER_SESSION_ID
C_Y = settings.CART_SESSION_KEY

class OrderViewTest(ProductTestMixin, TestCase):



    def test_get(self):
        url = reverse('order:form-order')
        res = self.client.get(url)
        self.assertTrue(res.status_code == 200)

    def get_data(self):
        s = mommy.make(Shipping)
        data = {'email': 'test@mail.ru',
                'first_name': 'test',
                'last_name': 'test',
                'country': 'test',
                'city': 'test',
                'address': 'test',
                'postal_code': 'test',
                'shipping': s.id}
        return data

    def session_set_data(self):
        session = self.client.session
        orders = session[C_Y] = {}
        p = self.create_product()
        for i in p.variant_set.all():
            orders[str(i.id)] = 1
        session.save()


    def test_post(self):
        data = self.get_data()
        url = reverse('order:form-order')
        self.session_set_data()
        res = self.client.post(url, data=data)
        self.assertTrue(res.status_code == 302)
        order = OrderModel.objects.get(email='test@mail.ru')
        self.assertTrue(self.client.session['order_id'] == order.id)
        for i in data:
            field_data = getattr(order, i, None)
            if i == 'shipping':
                field_data = field_data.id
            self.assertTrue(field_data==data[i])

    def test_without_session_data_post(self):
        data = self.get_data()
        url = reverse('order:form-order')
        res = self.client.post(url, data=data)
        self.assertFalse(res.status_code == 302)

class OrderPaymentPageViewTest(TestCase):

    def setUp(self):
        o = mommy.make(OrderModel)
        self.order_id = o.id

    def test_get(self):
        url = reverse('order:order-pay-page')
        session = self.client.session


        session[O_I] = self.order_id
        session.save()
        res = self.client.get(url)
        self.assertTrue(res.status_code == 200)

        del session[O_I]
        session.save()
        res = self.client.get(url)
        self.assertTrue(res.status_code == 404)
