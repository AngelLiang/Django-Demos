from django.contrib import admin

from .base import BaseAdmin
from ..models import State, TransitionMeta, TransitionApprovalMeta
from ..forms import WorkflowForm, TransitionMetaForm, TransitionApprovalMetaForm


class StateInline(admin.TabularInline):
    model = State
    fields = ('code', 'name', 'is_start', 'is_stop', 'weight')
    extra = 0
    show_change_link = True


class TransitionMetaInline(admin.TabularInline):
    model = TransitionMeta
    fields = ('source_state', 'destination_state', 'weight',)
    extra = 0
    ordering = ('weight',)
    show_change_link = True
    form = TransitionMetaForm


class TransitionApprovalMetaInline(admin.TabularInline):
    model = TransitionApprovalMeta
    fields = ('name', 'transition_meta', 'parents', 'weight')
    extra = 0
    # 如果按 parents 排序，当有多个 parents 时会出现重复的数据
    ordering = ('weight', 'id')
    show_change_link = True
    form = TransitionApprovalMetaForm


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
        # ('status_field',),

        ('is_active',),
        ('weight',),
    )
    readonly_fields = (
        'content_type', 'app_label',
        'model_name', 'status_field',
    )

    inlines = (StateInline, TransitionMetaInline, TransitionApprovalMetaInline)

    form = WorkflowForm
