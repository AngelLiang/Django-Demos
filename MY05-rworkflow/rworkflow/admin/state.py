
from .base import BaseAdmin
from django.utils.translation import ugettext_lazy as _


class StateAdmin(BaseAdmin):
    CODE_PREFIX = 'S'
    CODE_NUMBER_WIDTH = 3

    list_display = (
        'code', 'name', 'workflow',
        'is_start', 'is_stop', 'weight',
    )
    list_filter = ('workflow',)
    ordering = ('workflow', 'weight', 'code')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'workflow',
            ),
        }),
        (_('信息'), {
            'fields': (
                'code',
                ('is_active', 'is_start', 'is_stop',),
                'weight',
            ),
        }),

        (_('工单状态'), {
            'fields': (
                ('can_edit', 'can_suggestion', 'is_suggestion_required', 'need_take'),
            ),
        }),
    )
