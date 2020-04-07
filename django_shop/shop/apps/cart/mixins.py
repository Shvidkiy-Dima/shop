from .utils import CartObj
from shop.apps.core.models import Variant

class CartMixin:
    event = None
    product_model = Variant

    def dispatch(self, request, *args, **kwargs):
        self.cart = CartObj(request)
        self.extra_context = {'cart_obj': self.cart}
        return super().dispatch(request, *args, **kwargs)

    def cart_dispatch(self, req, event, *args):
        product_id = req.POST.get('id')
        self.cart.action(event, product_id)
        kwargs = {'count': self.cart.count}
        if event in ['add', 'delete']:
            count = self.cart.orders.get(product_id)
            p = self.product_model.objects.get(id=product_id)
            kwargs.update({'count_order': self.cart.count_order(product_id), 'extra': [p.count < count, p.count],
                           'price': p.price * count})
        return kwargs
