from django.contrib import admin
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
        # 'positions', 'roles', 'orgunits',
    )
    radio_fields = {'handler_type': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'workflow',
                'parents',
                ('can_edit', 'can_take',),
                ('email_notice', 'short_message_notice', 'weixin_notice'),
                'handler_type',
                'users',
            ),
        }),
    )
