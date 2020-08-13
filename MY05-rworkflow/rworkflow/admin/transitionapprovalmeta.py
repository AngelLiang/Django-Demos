from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .base import BaseAdmin


class TransitionApprovalMetaAdmin(BaseAdmin):
    CODE_PREFIX = 'TAM'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'priority')
    list_filter = ('workflow',)
    ordering = ('workflow', 'priority')

    filter_horizontal = (
        'parents',
        'users',
        'positions', 'roles', 'orgunits',
    )
    radio_fields = {'handler_type': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (
                # 'name',
                'workflow',
                'transition_meta',
                'parents',
            ),
        }),
        (_('通知'), {
            'fields': (
                ('email_notice', 'short_message_notice', 'weixin_notice'),
            ),
        }),
        (_('处理类型'), {
            'fields': (
                'handler_type',
                'positions',
                'roles',
                'users',
                'orgunits',
                'user_handler_function',
                'user_handler_sql',
            ),
        }),
    )
