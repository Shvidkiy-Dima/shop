from django.core.files.base import ContentFile
from model_mommy import mommy

from shop.apps.core.models import Product, Variant

import os

TEST_IMAGE = os.environ.get('TEST_IMG')


if os.environ.get('PROJECT_TEST') == 'PRODUCTION':
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    driver = webdriver.Remote(
          command_executor='http://selenium:4444/wd/hub',
          desired_capabilities=DesiredCapabilities.CHROME)
    WebDriver = (lambda: driver)
else:
    from selenium.webdriver.firefox.webdriver import WebDriver
    WebDriver = WebDriver



class ProductTestMixin:

    def create_product(self, price=40, variants=6, count_variants=6, sales=0):
        image = open(TEST_IMAGE, 'rb').read()
        image = ContentFile(image)
        product = mommy.make(Product, average_price=price)
        product.image.save('test_photo.jpg', image)
        for i in range(variants):
            mommy.make(Variant, product=product,  price=price, count=count_variants, sales=sales)
        return product

