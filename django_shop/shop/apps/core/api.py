from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import Product
from shop.apps.core.mixins import KeyFromQueryStringMixin



class DetailProductAPI(KeyFromQueryStringMixin, ModelViewSet):
    lookup_query_key = 'pk'
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
