from django.urls import path
from . import views
from .admin import DetailOrderPDF, DetailOrder

app_name = 'order'
urlpatterns = [
    path('order/', views.OrderView.as_view(), name='form-order'),
    path('order/payment/', views.OrderPaymentPageView.as_view(), name='order-pay-page'),

    path('admin/order-detail/<int:pk>/', DetailOrder.as_view(), name='detail-order'),
    path('admin/order-detail-pdf/<int:pk>/', DetailOrderPDF.as_view(), name='detail-order-pdf')
]
