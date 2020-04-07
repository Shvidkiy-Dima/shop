from django.forms.models import ModelChoiceField
from django.utils.html import mark_safe
from django.conf import settings



class MyChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return mark_safe("<span class='mr-5 pr-5'>%s</span> <span class='ml-5 pl-5'>%s%s</span>" %
                         (obj, obj.price, settings.CUR_CURRENCY))
