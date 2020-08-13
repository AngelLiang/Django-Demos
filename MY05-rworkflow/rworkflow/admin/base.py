from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    view_on_site = False

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.updated_by = user.username
        if not change:
            obj.created_by = user.username
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.distinct()
