from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        rfs = list(self.readonly_fields)
        if hasattr(obj, 'created_at'):
            rfs.append('created_at')
        if hasattr(obj, 'updated_at'):
            rfs.append('updated_at')
        return rfs

    # def delete_queryset(request, queryset):
    #     """override"""
    #     for obj in queryset:
    #         obj.is_deleted = True
    #         obj.save()
