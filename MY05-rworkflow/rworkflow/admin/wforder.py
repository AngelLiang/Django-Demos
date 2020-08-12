
import logging

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.conf.urls import url
from django.contrib.admin.utils import quote

from .base import BaseAdmin
from .. import models

LOGGER = logging.getLogger(__name__)


class WforderAdmin(BaseAdmin):
    CODE_PREFIX = 'WO'
    CODE_NUMBER_WIDTH = 5

    fieldsets = (
        (None, {
            'fields': (
                'code',
                'title',
                'rstatus',
                ('workflow_category', 'workflow',),
                # 'workflow_instance',
                'description',
            ),
        }),
    )
    readonly_fields = ('code', 'rstatus',)

    def has_change_permission(self, request, obj=None):
        if obj:
            approval = obj.get_current_approval()
            if approval and approval.can_edit is False:
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

        next_state = get_object_or_404(models.State, pk=next_state_id)
        LOGGER.debug(f'next_state:{next_state}')

        workflow_instance = obj.get_workflow_instance()
        workflow_instance.approve(as_user=request.user, next_state=next_state)
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
                    LOGGER.debug(approvals)
                    for approval in approvals:
                        url = reverse(f'admin:wf_approve',
                                      kwargs={'object_id': obj.pk,
                                              'next_state_id': approval.transition.destination_state.pk})
                        value = f'{approval.transition.source_state} -> {approval.transition.destination_state}'
                        next_approvals.append({'value': value, 'url': url})
                    extra_context.update({'next_approvals': next_approvals})

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
