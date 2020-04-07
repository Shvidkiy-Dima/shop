from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings


from .models import OrderModel, OrderItem, Shipping
from .mixins import ExportToCSVMixin, ExportToPDFMixin
from django.views.generic import DetailView


class DetailOrder(DetailView):
    template_name = 'order/order.html'
    model = OrderModel


class DetailOrderPDF(ExportToPDFMixin, DetailView):
    model = OrderModel
    pdf_template = 'order/pdf-templates/order-pdf.html'

    def get(self, req, *args, **kwargs):
        context = {'order': self.get_object()}
        return self.to_pdf(context)


class OrderInline(admin.TabularInline):
    model = OrderItem
    exclude = ('date_update',)
    extra = 0

@admin.register(OrderModel)
class OrderAdmin(ExportToCSVMixin, admin.ModelAdmin):
    list_display = ('last_name', 'address', 'city', 'total_price', 'paid', 'get_date_create', 'OrderDetail', 'OrderDetailPDF')
    inlines = [OrderInline]
    actions = ['to_csv']
    csv_filename = 'orders.csv'

    def OrderDetailPDF(self, order):
        return format_html('<a href=%s>PDF</a>' % reverse('order:detail-order-pdf', kwargs={'pk': order.id}))
    OrderDetailPDF.short_description = 'PDF'

    def OrderDetail(self, order):
        return format_html('<a href=%s>Подробнее</a>' % reverse('order:detail-order', kwargs={'pk': order.id}))
    OrderDetail.short_description = 'Подробнее'


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ('id', 'price', 'date_create')
    search_fields = ('=id',)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    pass




