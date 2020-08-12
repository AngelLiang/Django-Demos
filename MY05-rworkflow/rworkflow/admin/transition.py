
from .base import BaseAdmin


class TransitionAdmin(BaseAdmin):
    list_display = ('__str__', 'workflow_object', 'iteration')
    ordering = ('content_type', 'object_id', 'iteration',)

    # readonly_fields = (
    #     'workflow', 'iteration',
    #     'content_type', 'object_id',
    # )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
