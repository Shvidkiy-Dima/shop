from django.forms import ModelForm, widgets

from .fields import MyChoiceField
from .models import Shipping
from .models import OrderModel

class OrderForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            p = f.capitalize().replace('_', ' ')
            self.fields[f].widget.attrs.update({'placeholder': p})
            self.fields[f].label = ''

    shipping = MyChoiceField(queryset=Shipping.objects.all(), empty_label=None, widget=widgets.RadioSelect())


    class Meta:
        model = OrderModel
        fields = ['first_name', 'last_name', 'address', 'country', 'city', 'postal_code', 'email', 'shipping']

