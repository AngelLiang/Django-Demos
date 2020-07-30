from django.contrib import admin

from .base import BaseAdmin
from ..models import State, TransitionMeta, TransitionApprovalMeta
from ..forms import WorkflowForm


class StateInline(admin.TabularInline):
    model = State
    fields = ('code', 'name', 'is_start', 'is_stop')
    extra = 0


class TransitionMetaInline(admin.TabularInline):
    model = TransitionMeta
    fields = ('source_state', 'destination_state', 'weight',)
    extra = 0
    ordering = ('weight',)


class TransitionApprovalMetaInline(admin.TabularInline):
    model = TransitionApprovalMeta
    fields = ('transition_meta', 'parents', 'priority')
    extra = 0
    ordering = ('priority', 'parents')


class WorkflowAdmin(BaseAdmin):
    CODE_PREFIX = 'WF'
    CODE_NUMBER_WIDTH = 3

    # raw_id_fields = ('content_type', )
    fields = (
        ('name',),
        ('rstatus',),
        # ('content_type', 'object_id',),
        ('content_type',),
        ('app_label', 'model_name',),
        ('status_field',),
        ('order_relation_config',),

        ('is_inuse',),
        ('weight',),
    )
    # readonly_fields = ('app_label', 'model_name',)
    readonly_fields = ('content_type', 'app_label', 'model_name', 'status_field',)

    inlines = (StateInline, TransitionMetaInline, TransitionApprovalMetaInline)

    form = WorkflowForm
