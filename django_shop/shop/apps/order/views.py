from django.views.generic import CreateView, DetailView
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import OrderModel
from shop.apps.cart.mixins import CartMixin
from .forms import OrderForm


O_I = settings.ORDER_SESSION_ID


class OrderView(CartMixin, CreateView):
    model = OrderModel
    form_class = OrderForm
    template_name = 'order/order_form.html'

    def form_valid(self, form):
        if self.cart.is_empty():
            return self.form_invalid(form)

        response = super().form_valid(form)
        self.object.set_items(self.cart)
        self.cart_dispatch(self.request, 'clear')

        if self.request.session.get(O_I):
            OrderModel.objects.filter(id=self.request.session[O_I]).delete()
        self.request.session[O_I] = self.object.id

        return response


class OrderPaymentPageView(DetailView):
    template_name = 'order/order_payment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(OrderModel, **{'id': self.request.session.get(O_I),
                                                'paid': False})









