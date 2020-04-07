from django.http.response import JsonResponse

class JsonResponseMixin:
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        data = super().dispatch(request, *args, **kwargs)
        return data if not request.is_ajax() else JsonResponse(data)


    def get(self, req, *args, **kwarg):
        return super().get(req, *args, **kwarg) if not req.is_ajax() else self.get_json_data(req, *args, **kwarg)


class KeyFromQueryStringMixin:
    lookup_query_key = 'pk'

    def dispatch(self, request, *args, **kwargs):
        value = request.GET.get(self.lookup_query_key)
        if value:
            self.kwargs.update({self.lookup_query_key: value})
        return super().dispatch(request, *args, **self.kwargs)






