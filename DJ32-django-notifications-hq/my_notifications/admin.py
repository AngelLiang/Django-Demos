from django.contrib import admin

from .models import MyNotification


class MyNotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ('recipient',)
    list_display = ('recipient', 'actor',
                    'level', 'target', 'unread', 'public')
    list_filter = ('level', 'unread', 'public', 'timestamp',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(recipient=request.user)
        return qs


admin.site.register(MyNotification, MyNotificationAdmin)
