from django.test import TestCase
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from .main import ProductTestMixin

class MainPageViewTest(TestCase):

    def test_get(self):
        url = reverse('core:main-page')
        res = self.client.get(url)
        self.assertTrue(isinstance(res, HttpResponse))


    def test_api_ajax(self):
        url = reverse('core:products')
        res = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(isinstance(res, JsonResponse))


class DetailProductViewTest(ProductTestMixin, TestCase):

    def setUp(self):
        self.product = self.create_product()

    def test_get(self):
        url = reverse('core:detail-product-main', kwargs={'slug': self.product.id})
        res = self.client.get(url)
        self.assertTrue(isinstance(res, HttpResponse))

    def test_api_ajax(self):
        url = reverse('core:detail-product')
        res = self.client.get(url, data={'pk': self.product.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(isinstance(res, JsonResponse))
