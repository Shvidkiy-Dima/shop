from django.core.management.base import BaseCommand
from shop.apps.core.models import Product,  Variant, Brand, Category
from django.core.files.base import ContentFile
import os

DEFAULT_IMG = os.environ.get('DEFAULT_IMG') or '/project/django_shop/shop/apps/core/static/testimg.jpeg'


class Command(BaseCommand):

    def handle(self, count=50,  **options):
        for i in range(1, count):
            image = open(DEFAULT_IMG, 'rb').read()
            image = ContentFile(image)
            brand = Brand.objects.create(name='Test brand %s' % i)
            category = Category.objects.create(name='Test category %s' % i)
            a_p = sum(i*(n+1) for n in range(4)) // 4
            product = Product(category=category,
                                             brand=brand, name='test product% s' % i, average_price=a_p)
            product.image.save('test_photo.jpg', image)
            for n, j in enumerate(['L', 'M', 'XL', 'XXL']):
                price = i*(n+1)
                Variant.objects.create(product=product, count=count, price=price, size=j)
            print('Product %s create!' % product.id)

