from django.contrib import admin

from .models import AuthEntry


@admin.register(AuthEntry)
class AuthEntryAdmin(admin.ModelAdmin):
    list_display = ['username', 'action', 'action_at', 'ip', ]
    # list_display = ['__str__', 'ip']
    list_filter = ['action', 'action_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
