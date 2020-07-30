
from .base import BaseAdmin

from django.contrib.contenttypes.models import ContentType


class WforderAdmin(BaseAdmin):
    CODE_PREFIX = 'WO'
    CODE_NUMBER_WIDTH = 5

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        opts = self.opts
        app_label = opts.app_label
        model_name = opts.model_name

        workflow = None
        workflow_instance = None

        if object_id:
            # 获取对象
            obj = self.get_object(request, object_id)
            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

            workflow = self.get_workflow(request, obj)
            # print(workflow)
            extra_context.update({'workflow': workflow})
            if workflow:
                workflow_instance = self.get_workflow_instance(request, obj, workflow)
                print(workflow_instance)
                extra_context.update({'workflow_instance': workflow_instance})

        return super().changeform_view(request, object_id, form_url, extra_context)

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
            content_type = ContentType.objects.get(app_label=WORKFLOW_APP_LABEL, model=WORKFLOW_MODEL_NAME)
            workflow = content_type.get_object_for_this_type(app_label=app_label, model_name=model_name)
        except Exception:
            return None
        return workflow

    def get_workflow_instance(self, request, obj, workflow):
        from ..models import WorkflowInstance
        WORKFLOW_APP_LABEL = 'rworkflow'
        WORKFLOWINSTANCE_MODEL_NAME = 'workflowinstance'
        try:
            content_type = ContentType.objects.get(app_label=WORKFLOW_APP_LABEL, model=WORKFLOWINSTANCE_MODEL_NAME)
            workflow_instance = content_type.get_object_for_this_type(workflow=workflow, object_id=obj.id)
        except Exception:
            pass
            workflow_instance = WorkflowInstance.objects.create(
                workflow=workflow,
                object_id=obj.id,
                starter=request.user,
            )
        workflow_instance.initialize_approvals()
        return workflow_instance
