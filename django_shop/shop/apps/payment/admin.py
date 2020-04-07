from django.contrib import admin
from .models import PayRecord


@admin.register(PayRecord)
class PayReordAdmin(admin.ModelAdmin):
    list_display = ('payment_system', 'client', 'price', 'get_date_create')

