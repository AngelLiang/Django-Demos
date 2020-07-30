
from .base import BaseAdmin


class TransitionAdmin(BaseAdmin):
    list_display = ('__str__', 'workflow_object', 'iteration')
    ordering = ('content_type', 'object_id', 'iteration',)
