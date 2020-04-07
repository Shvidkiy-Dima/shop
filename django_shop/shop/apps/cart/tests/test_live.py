from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from shop.apps.core.tests.main import WebDriver, ProductTestMixin


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import socket, time




class TestCartActions(ProductTestMixin, StaticLiveServerTestCase):
    host = '0.0.0.0'


    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())

    def setUp(self):
        super().setUpClass()
        self.driver = WebDriver()
        self.create_product()



    def wait(self, expr):
        try:
            WebDriverWait(self.driver, 10).until(expr)
        except (NoSuchElementException, TimeoutException):
            return False
        else:
            return True

    def test_add_in_cart(self):
        self.driver.get(self.live_server_url)

        b = self.wait(EC.element_to_be_clickable((By.XPATH,'.//a[@data-action="detail-product"]')))

        self.assertTrue(b, msg='Error: product was not found')

        self.assertTrue(int(self.driver.find_element_by_id('cart-counter').text) == 0)

        #Открыл модальное окно с товаром
        self.driver.find_element_by_xpath('.//a[@data-action="detail-product"]').click()
        time.sleep(2)


        b = self.wait(EC.presence_of_element_located(
            (By.XPATH, './/div[@id="base-shop-modal"]//button[@data-action="order-product"]')))

        self.assertTrue(b, msg='Error: order error')

        # Добаил в корзину
        self.driver.find_element_by_xpath('.//div[@id="base-shop-modal"]//button[@data-action="order-product"]').click()

        time.sleep(2)

        b = self.wait(EC.element_to_be_clickable((By.XPATH, './/a[@id="my-cart"]')))

        self.assertTrue(b, msg='Error: cart was not found')


        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/span[@id="cart-counter" and contains(text(), 1)]')))

        self.assertTrue(b, msg='Error: cart counter dont increment')

        # Открыл корзину
        self.driver.find_element_by_id('my-cart').click()

        b = self.wait(EC.presence_of_element_located((By.XPATH,
                                                       './/div[@id="my-cart-modal"]//tr[@data-id="body-product-cart"]')))
        self.assertTrue(b, msg='Error: product not in cart')

        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/div[@id="my-cart-modal"]'
            '//tr[@data-id="body-product-cart"]'
            '//span[@data-id="cart-counter-product" and contains(text(), 1)]')))

        self.assertTrue(b, msg='Error: wrong count in cart')

        # Добавил еще одну едницу товара
        self.driver.find_element_by_xpath('.//div[@id="my-cart-modal"]'
                                          '//tr[@data-id="body-product-cart"]'
                                          '//button[@data-action="order-product"]').click()

        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/div[@id="my-cart-modal"]'
            '//tr[@data-id="body-product-cart"]'
            '//span[@data-id="cart-counter-product" and contains(text(), 2)]')))

        self.assertTrue(b, msg='Error: Counter dont increment')

        # Отнял одну едницу товара
        self.driver.find_element_by_xpath('.//div[@id="my-cart-modal"]'
                                          '//tr[@data-id="body-product-cart"]'
                                          '//button[@data-action="delete-cart-product"]').click()

        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/div[@id="my-cart-modal"]'
            '//tr[@data-id="body-product-cart"]'
            '//span[@data-id="cart-counter-product" and contains(text(), 1)]')))

        self.assertTrue(b, msg='Error: Counter dont decrement')

        # Проверил, что кол-во единиц товара не может быть меньше одного
        self.driver.find_element_by_xpath('.//div[@id="my-cart-modal"]'
                                          '//tr[@data-id="body-product-cart"]'
                                          '//button[@data-action="delete-cart-product"]').click()

        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/div[@id="my-cart-modal"]'
            '//tr[@data-id="body-product-cart"]'
            '//span[@data-id="cart-counter-product" and contains(text(), 1)]')))

        self.assertTrue(b, msg='Error: counter after operation delete == 0')

        # Удалил товар
        self.driver.find_element_by_xpath('.//div[@id="my-cart-modal"]'
                                          '//tr[@data-id="body-product-cart"]'
                                          '//a[@data-action="delete-cart-product-all"]').click()
        time.sleep(3)
        b = self.wait((lambda _: self.driver.find_element_by_xpath(
            './/div[@id="my-cart-modal"]'
            '//tr[@data-id="body-product-cart"]')))

        self.assertFalse(b, msg='Error: product was not delete after operation delete-all')


    def tearDown(self):
        self.driver.close()