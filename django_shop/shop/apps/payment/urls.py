from . import views

from django.urls import path, include



app_name = 'payment'
urlpatterns = [

    path('stripe-pay/', views.StripePay.as_view(), name='stripe-pay'),

    path('done/', views.PaymentResult.as_view(template_name='payment/done.html'), name='done'),
    path('canceled/', views.PaymentResult.as_view(template_name='payment/cancel.html'), name='cancel')
]