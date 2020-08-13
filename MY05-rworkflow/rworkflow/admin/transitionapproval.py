
from .base import BaseAdmin
from django.utils.translation import ugettext_lazy as _


class TransitionApprovalAdmin(BaseAdmin):
    CODE_PREFIX = 'TA'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'workflow_object', 'status', 'previous', 'weight')
    list_filter = ('status',)
    ordering = ('content_type', 'object_id', )

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'workflow',
                'workflow_object',
                'meta',
                'status',
            ),
        }),
        (_('流转信息'), {
            'fields': (
                'previous',
                'transactioner',
                'transaction_at',
                'memo',
                'weight',
            ),
        }),

        (_('通知'), {
            'fields': (
                ('email_notice', 'short_message_notice', 'weixin_notice'),
            ),
        }),
        (_('处理者'), {
            'fields': (
                ('users',),
            ),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
