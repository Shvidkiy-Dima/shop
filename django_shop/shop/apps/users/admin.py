from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.set_password(obj.password)
        obj.save()