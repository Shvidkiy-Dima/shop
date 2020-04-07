from django.urls import path
from . import views, api

app_name = 'core'
urlpatterns = [
    path('', views.MainPageView.as_view(template_name='core/mainpage.html'), name='main-page'),
    path('detail-product/<slug:slug>/', views.DetailProductView.as_view(template_name='core/detail-product-main.html'),
                                                                                            name='detail-product-main'),

    path('api/products/', views.MainPageView.as_view(template_name='core/objects/products.html'), name='products'),
    path('api/detail-product/', views.DetailProductView.as_view(template_name='core/objects/detail-product.html'),
                                                                                            name='detail-product'),
]
