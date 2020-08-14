from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .base import BaseAdmin
from .. import models
from ..models import State, TransitionMeta, TransitionApprovalMeta
from ..forms import WorkflowForm, TransitionMetaForm, TransitionApprovalMetaForm


class StateInline(admin.TabularInline):
    model = models.State
    fields = ('code', 'name', 'is_start', 'is_stop', 'weight')
    extra = 0
    show_change_link = True


class TransitionMetaInline(admin.TabularInline):
    model = models.TransitionMeta
    fields = ('source_state', 'destination_state', 'weight',)
    extra = 0
    ordering = ('weight',)
    show_change_link = True
    form = TransitionMetaForm


class TransitionApprovalMetaInline(admin.TabularInline):
    model = models.TransitionApprovalMeta
    fields = ('name', 'transition_meta', 'parents', 'weight')
    extra = 0
    # 如果按 parents 排序，当有多个 parents 时会出现重复的数据
    ordering = ('weight', 'id')
    show_change_link = True
    form = TransitionApprovalMetaForm


class ExtraParamMetaInline(admin.TabularInline):
    model = models.ExtraParamMeta
    fields = ('name', 'is_active', 'value_tp', 'required', 'memo', 'weight')
    ordering = ('weight', 'id')
    extra = 0
    show_change_link = True


class WorkflowAdmin(BaseAdmin):
    CODE_PREFIX = 'WF'
    CODE_NUMBER_WIDTH = 3

    # raw_id_fields = ('content_type', )
    # fields = (
    #     ('name',),
    #     ('rstatus',),
    #     # ('content_type', 'object_id',),
    #     ('content_type',),
    #     ('app_label', 'model_name',),
    #     # ('status_field',),

    #     ('is_active',),
    #     ('weight',),
    # )
    fieldsets = (
        (None, {
            'fields': (
                ('name',),
                ('rstatus',),
            ),
        }),
        (_('信息'), {
            'fields': (
                ('content_type',),
                ('app_label', 'model_name',),
                ('is_active',),
                ('weight',),
            ),
        }),
    )

    readonly_fields = (
        'content_type', 'app_label',
        'model_name', 'status_field',
    )

    inlines = (StateInline, TransitionMetaInline, TransitionApprovalMetaInline, ExtraParamMetaInline)

    form = WorkflowForm
