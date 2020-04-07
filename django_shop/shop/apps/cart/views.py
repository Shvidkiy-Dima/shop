from django.views.generic import View
from django.template.loader import render_to_string

from .mixins import CartMixin
from shop.apps.core.mixins import JsonResponseMixin



class CartView(JsonResponseMixin, CartMixin, View):

    def get(self, req, *args, **kwargs):
        return {'html': render_to_string(self.template_name, self.extra_context)}


    def post(self, req, *args, **kwargs):
        return self.cart_dispatch(req, self.event)


