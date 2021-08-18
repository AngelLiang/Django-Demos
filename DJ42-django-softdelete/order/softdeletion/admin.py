from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class SoftDeletionAdminMixin(admin.ModelAdmin):

    def make_recover_action(self, request, queryset):
        items = queryset.all()
        for item in items:
            item.recover()
        self.message_user(request, _(f'恢复成功，一共恢复 {len(items)} 个'), messages.SUCCESS)
    make_recover_action.allowed_permissions = ('delete',)
    make_recover_action.short_description = _('恢复所选的数据')

    # def has_publish_permission(self, request):
    #     """Does the user have the publish permission?"""
    #     opts = self.opts
    #     codename = get_permission_codename('delete', opts)
    #     return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    actions = ['make_recover_action']


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
