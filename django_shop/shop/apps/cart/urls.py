from django.urls import path
from . import views

urlpatterns = [
    path('put/', views.CartView.as_view(event='add'), name='put-in-cart'),
    path('delete/', views.CartView.as_view(event='delete'), name='delete-from-cart'),
    path('delete-all/', views.CartView.as_view(event='delete_all'), name='delete-from-cart-all'),
    path('check/', views.CartView.as_view(template_name='cart/objects/cart_object.html'), name='check-cart')
]