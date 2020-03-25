from django.contrib import messages
from django.contrib import admin

# Register your models here.
from . import models


class RemoveAdminDefaultMessageMixin:

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        """override"""
        response = super().response_change(request, obj)
        self.remove_default_message(request)
        return response

    def response_delete(self, request, obj_display, obj_id):
        """override"""
        response = super().response_delete(request, obj_display, obj_id)
        self.remove_default_message(request)
        return response


class MessageAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        self.message_user(request, '保存成功！')
        return super().save_model(request, obj, form, change)


admin.site.register(models.Message, MessageAdmin)
