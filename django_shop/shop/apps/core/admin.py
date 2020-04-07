from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext as _
from django.db.models import Sum

from .models import Product, Category, Brand, Variant



class AdminMixin:
    exclude = ['slug']



class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


@admin.register(Product)
class ProductAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('name', 'category', 'brand',  'average_price', 'features', 'get_count', 'sales', 'last_sale')
    ordering = ['-variant__sales', '-variant__last_sale']
    inlines = [VariantInline]
    list_filter = ['date_create', 'variant__last_sale']

    def sales(self, product):
        return str(product.get_sales())

    def last_sale(self, product):
        v = product.variant_set.order_by('-last_sale').first()
        return v.last_sale.strftime(settings.ADMIN_DATE_FORMAT)


    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        f = formsets[0].save()
        if not formsets[0].queryset.exists() and not f:
            Variant.objects.create(product=form.instance, price=form.instance.average_price)



@admin.register(Category)
class CategoryAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('name', 'sales')


    def sales(self, category):
        s = category.product_set.aggregate(sales=Sum('variant__sales'))
        return str(s['sales'])



@admin.register(Brand)
class BrandAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('name', 'sales')


    def sales(self, brand):
        s = brand.product_set.aggregate(sales=Sum('variant__sales'))
        return str(s['sales'])







