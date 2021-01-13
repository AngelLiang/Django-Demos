from django.contrib import admin
from .models import CustomModel


@admin.register(CustomModel)
class CustomModelAdmin(admin.ModelAdmin):
    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        cl.title = ('自定义页面')
        return cl
