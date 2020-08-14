
from .base import BaseAdmin
from ..forms import TransitionMetaForm


class TransitionMetaAdmin(BaseAdmin):
    CODE_PREFIX = 'TM'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'workflow', 'weight',)
    list_filter = ('workflow',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'workflow',
                ('source_state', 'destination_state',),
                'weight',
            ),
        }),
    )
    readonly_fields = ('workflow',)
    form = TransitionMetaForm
