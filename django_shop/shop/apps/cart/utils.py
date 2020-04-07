from django.conf import settings

from shop.apps.core.models import Variant



CART_SESSION_KEY = settings.CART_SESSION_KEY
MAX_CART_SIZE = settings.MAX_CART_SIZE

class CartObj:
    def __init__(self, request):
        self.session = request.session
        self.orders = request.session.setdefault(CART_SESSION_KEY, {})
        self.items = None


    def get_items(self):
        if not self.items:
            pk = [key for key, _ in self]
            self.items = Variant.objects.filter(id__in=pk)
        for v in self.items:
            yield v, self.orders[str(v.id)], self.exceed(v)

    def __iter__(self):
       yield from self.orders.items()

    def action(self, event, id):
        """type(id) == str"""
        self.session.modified = True
        return getattr(self, '_'+event)(str(id))


    def _add(self, id):
        if self.orders.get(id):
            self.orders[id] += self.orders[id] < MAX_CART_SIZE
        else:
            self.orders[id] = 1

    def _delete(self, id):
        self.orders[id] -= self.orders[id] > 1

    def _delete_all(self, id):
        del self.orders[id]
        if self.items: self.items = self.items.exclude(id=id)

    def _clear(self, _):
        self.orders.clear()
        self.items = None

    def exceed(self, variant):
        return variant.count < self.orders[str(variant.id)]

    def count_order(self, id):
        return self.orders.get(str(id))

    def is_empty(self):
        return not bool(self.orders)

    @property
    def count(self):
        return sum((val for _, val in self))


    @property
    def total_price(self):
        return sum((float(obj.price)*count for obj, count, exceed in self.get_items() if not exceed))