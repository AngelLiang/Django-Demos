
from .base import BaseAdmin


class TransitionMetaAdmin(BaseAdmin):
    CODE_PREFIX = 'TM'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'weight',)
    list_filter = ('workflow',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'workflow',
                'source_state',
                'destination_state',
                'weight',
            ),
        }),
    )
