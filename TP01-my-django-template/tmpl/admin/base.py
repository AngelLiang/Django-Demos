from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if hasattr(obj, 'created_at'):
            readonly_fields.append('created_at')
        if hasattr(obj, 'updated_at'):
            readonly_fields.append('updated_at')
        return readonly_fields
