
from .base import BaseAdmin


class StateAdmin(BaseAdmin):
    CODE_PREFIX = 'S'
    CODE_NUMBER_WIDTH = 3

    list_display = ('code', 'name', 'workflow', 'status_value', 'is_start', 'is_stop', 'weight',)
    list_filter = ('workflow',)
    ordering = ('workflow', 'weight', 'code')
