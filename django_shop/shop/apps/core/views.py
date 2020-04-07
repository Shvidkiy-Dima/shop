from django.views.generic import DetailView
from django_filters.views import FilterView
from django.template.loader import render_to_string

from .filters import ProductFilter
from .mixins import KeyFromQueryStringMixin, JsonResponseMixin
from .models import Product




class MainPageView(JsonResponseMixin, FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 8

    def get_json_data(self, req, *args, **kwarg):
        super(JsonResponseMixin, self).get(req, *args, **kwarg)
        return {'html':
                render_to_string(self.template_name, super().get_context_data(object_list=self.object_list))}


class DetailProductView(JsonResponseMixin, KeyFromQueryStringMixin, DetailView):
    model = Product

    def get_json_data(self, *args, **kwargs):
        return {'html':
                render_to_string(self.template_name, {'product': self.get_object()})}

