
from .base import BaseAdmin


class TransitionApprovalAdmin(BaseAdmin):
    CODE_PREFIX = 'TA'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'workflow_object', 'status', 'previous')
    list_filter = ('status',)
    ordering = ('content_type', 'object_id', )

    fieldsets = (
        (None, {
            'fields': (
                'workflow',
                'workflow_object',
                'previous',
                'status',
                'transactioner',
                'transaction_at',
                'memo',
                'meta',
                ('can_edit', 'can_take',),
                ('email_notice', 'short_message_notice', 'weixin_notice'),
                'users',
            ),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
