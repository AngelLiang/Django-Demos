from django.contrib import admin


class SoftDeletionAdminMixin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.delete()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 超级管理员能查看所有数据
        if request.user.is_superuser:
            return self.model.objects.all()
        return qs.filter(is_deleted=False)
