
from .base import BaseAdmin


class TransitionApprovalAdmin(BaseAdmin):
    CODE_PREFIX = 'TA'
    CODE_NUMBER_WIDTH = 3

    list_display = ('__str__', 'workflow_object', 'status', 'previous')
    ordering = ('content_type', 'object_id', )
