from django.utils.translation import gettext as _
from django.forms import widgets

from .models import Product, Brand, Category

import django_filters




CHOICES =[
        ["name", "по алфавиту"],
        ["average_price", "дешевые сверху"],
        ["-average_price", "дорогие сверху"]
]

class ProductFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(choices=CHOICES, required=True, empty_label=None, label=_('Сортировать'))

    average_price__lt = django_filters.NumberFilter(field_name='average_price', lookup_expr='lt', label= 'Цена ниже',
                                                    widget=widgets.NumberInput(attrs={'placeholder': '$'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), empty_label='Категория', label='')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='',
                                                     widget=widgets.TextInput(attrs={'placeholder': 'Поиск' }))
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(),  empty_label=_('Бренд'), label='')

    class Meta:
        model = Product
        fields = []

