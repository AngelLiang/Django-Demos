
import logging

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.conf.urls import url
from django.contrib.admin.utils import quote
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from .base import BaseAdmin
from .. import models
from ..tables import TransitionApprovalTable
from ..forms import ExtraParamForm


LOGGER = logging.getLogger(__name__)


class WfOrderRelatedListFilter(admin.SimpleListFilter):

    title = _('工单关系')
    parameter_name = 'wo'

    def lookups(self, request, model_admin):
        return (
            ('mine', _('我创建的')),
            ('todo', _('我的待办')),
            ('related', _('与我相关')),
            ('done', _('处理完成')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        user = request.user
        if value == 'mine':
            # 我创建的
            return queryset.filter(user=user)
        elif value == 'todo':
            # 我的待办
            approvals = models.TransitionApproval.objects.filter(
                status=models.TransitionApproval.PENDING,
                users__id=user.id
            )
            ids = approvals.values_list('object_id', flat=True).distinct()
            return queryset.filter(id__in=ids)
        elif value == 'related':
            # 与我相关：等待我处理的和我处理完成的工单
            approvals = models.TransitionApproval.objects.filter(
                status__in=(models.TransitionApproval.PENDING, models.TransitionApproval.APPROVED),
                users__id=user.id
            )
            ids = approvals.values_list('object_id', flat=True).distinct()
            return queryset.filter(id__in=ids)
        elif value == 'done':
            # 处理完成
            approvals = models.TransitionApproval.objects.filter(
                status=models.TransitionApproval.APPROVED,
                users__id=user.id
            )
            ids = approvals.values_list('object_id', flat=True).distinct()
            return queryset.filter(id__in=ids)

        return queryset


class ExtraParamInline(admin.TabularInline):
    model = models.ExtraParam
    fields = ('name', 'value_tp', 'paramvalue', 'memo',)
    ordering = ('weight', 'id')
    readonly_fields = ('name', 'value_tp', 'memo',)
    extra = 0
    # can_delete = False
    # show_change_link = True
    form = ExtraParamForm

    # def get_fields(self, request, obj=None):
    #     # self.model.filter(wo=obj)
    #     fields = list(super().get_fields(request, obj))
    #     if obj:
    #         value_attr = obj.gen_value_attr()
    #         fields.append(value_attr)
    #     return fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def paramvalue(self, request, obj=None):
    #     return None


class WforderAdmin(BaseAdmin):
    CODE_PREFIX = 'WO'
    CODE_NUMBER_WIDTH = 5

    list_display = ('code', 'title', 'workflow', 'rstatus', 'applier')
    list_display_links = ('code', 'title',)
    list_filter = (WfOrderRelatedListFilter, 'workflow', )
    fieldsets = (
        (None, {
            'fields': (
                ('code', 'rstatus',),
                'title',
                ('workflow_category', 'workflow',),
                # 'workflow_instance',
                'description',
            ),
        }),
    )
    readonly_fields = ('code', 'rstatus',)
    inlines = (ExtraParamInline,)

    def get_readonly_fields(self, request, obj):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])

        if obj and obj.is_wf_start():
            readonly_fields.append('workflow_category')
            readonly_fields.append('workflow')
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        """
        - 流程初始状态下，根据状态所配置的编辑权限来确定申请人是否可编辑
        - 其他状态下，根据工单当前的状态来判断处理人是否可以编辑，其他人不可编辑
        """
        user = request.user
        if obj:
            if obj.is_on_initial_state():
                return obj.can_edit()
            # users = obj.get_current_handle_users() or []
            # if user in users:
            #     return obj.can_edit()
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_wf_start():
            return False
        return super().has_delete_permission(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        return [
            url(r'^(?P<object_id>\d+)/wf_approve/(?P<next_state_id>\d+)/$',
                self.wf_approve_api, name='wf_approve'),
        ] + urls

    def wf_approve_api(self, request, object_id, next_state_id=None):
        opts = self.opts
        app_label = opts.app_label
        model_name = opts.model_name

        if object_id:
            obj = self.get_object(request, object_id)
            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        memo = request.POST.get('memo', '')
        LOGGER.debug(memo)

        next_state = get_object_or_404(models.State, pk=next_state_id)
        LOGGER.debug(f'next_state:{next_state}')

        workflow_instance = obj.get_workflow_instance()
        workflow_instance.approve(as_user=request.user, next_state=next_state, memo=memo)

        # admin:<app>_<model>_change
        return redirect(
            reverse(f'admin:{app_label}_{model_name}_change',
                    args=(quote(obj.pk),),
                    current_app=self.admin_site.name)
        )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        user = request.user
        extra_context = extra_context or {}

        opts = self.opts
        app_label = opts.app_label
        model_name = opts.model_name

        if object_id:
            # 获取对象
            obj = self.get_object(request, object_id)
            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

            workflow = self.get_workflow(request, obj)
            extra_context.update({'workflow': workflow})
            if workflow:
                workflow_instance, is_created = obj.get_or_create_workflow_instance(request)
                extra_context.update({'workflow_instance': workflow_instance})

                if workflow_instance:
                    next_approvals = []
                    approvals = workflow_instance.get_available_approvals(user).all()
                    LOGGER.debug(f'approvals:{approvals}')
                    for approval in approvals:
                        url = reverse(f'admin:wf_approve',
                                      kwargs={'object_id': obj.pk,
                                              'next_state_id': approval.transition.destination_state.pk})
                        value = approval.name or f'{approval.transition.source_state} -> {approval.transition.destination_state}'
                        next_approvals.append({'value': value, 'url': url})

                    is_current_handle_user = obj.is_current_handle_user(user)
                    extra_context.update({
                        'is_current_handle_user': is_current_handle_user,
                        'next_approvals': next_approvals
                    })

        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        from django.http import HttpResponseRedirect
        user = request.user

        if '_workflow-start' in request.POST:
            LOGGER.debug('启动流程')
            # app_label, model_name = self.opts.app_label, self.opts.model_name
            # return HttpResponseRedirect(f'/admin/{app_label}/{model_name}/{obj.id}/change/start/')
            if obj.wf_start(request):
                self.message_user(request, '流程启动成功')
            return HttpResponseRedirect('.')

        return super().response_change(request, obj)

    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        opts = self.opts
        if object_id:
            # 获取对象
            obj = self.get_object(request, object_id)
            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

            approvals = obj.get_history_approvals()
            LOGGER.debug(approvals)

            approvals_table = TransitionApprovalTable(approvals.all())
            approvals_table.paginate(page=request.GET.get('page', 1), per_page=25)
            LOGGER.debug(approvals_table)
            extra_context.update(dict(approvals=approvals_table))

        return super().history_view(request, object_id, extra_context)

    def get_workflow(self, request, obj):
        workflow = getattr(obj, 'workflow', None)
        if workflow:
            return workflow

        opts = self.opts
        app_label = opts.app_label
        model_name = opts.model_name

        WORKFLOW_APP_LABEL = 'rworkflow'
        WORKFLOW_MODEL_NAME = 'workflow'
        try:
            content_type = ContentType.objects.get(
                app_label=WORKFLOW_APP_LABEL, model=WORKFLOW_MODEL_NAME)
            workflow = content_type.get_object_for_this_type(
                app_label=app_label, model_name=model_name)
        except Exception:
            return None
        return workflow

    def get_changeform_initial_data(self, request):
        return {
            'user': request.user
        }

    def save_model(self, request, obj, form, change):
        if obj.user is None:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            # 超级管理员能查看所有数据
            return qs

        qfilter = Q()
        qfilter |= Q(created_by=user.username)

        # 与我相关：等待我处理的和我处理完成的工单
        approvals = models.TransitionApproval.objects.filter(
            status__in=(models.TransitionApproval.PENDING, models.TransitionApproval.APPROVED),
            users__id=user.id
        )
        ids = approvals.values_list('object_id', flat=True).distinct()
        qfilter |= Q(id__in=ids)

        return qs.filter(qfilter)
