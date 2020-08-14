from django.contrib.contenttypes.models import ContentType

from .base import BaseManager


class TransitionApprovalManager(BaseManager):

    def filter(self, *args, **kwarg):
        workflow_object = kwarg.pop('workflow_object', None)
        if workflow_object:
            kwarg['content_type'] = ContentType.objects.get_for_model(workflow_object)
            kwarg['object_id'] = workflow_object.pk

        return super().filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        workflow_object = kwarg.pop('workflow_object', None)
        if workflow_object:
            kwarg['content_type'] = ContentType.objects.get_for_model(workflow_object)
            kwarg['object_id'] = workflow_object.pk

        return super().update_or_create(*args, **kwarg)
