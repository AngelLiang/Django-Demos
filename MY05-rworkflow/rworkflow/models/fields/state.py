import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete

# from river.core.riverobject import RiverObject
from rworkflow.core.workflowregistry import workflow_registry

from django.contrib.contenttypes.fields import GenericRelation

from rworkflow.models import State
from rworkflow.models import TransitionApproval
from rworkflow.models import Transition


LOGGER = logging.getLogger(__name__)


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(instance) if instance else self.getter(owner)


class StateField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        self.field_name = None
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['to'] = '%s.%s' % (State._meta.app_label, State._meta.object_name)
        kwargs['on_delete'] = kwargs.get('on_delete', models.CASCADE)
        kwargs['related_name'] = "+"
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        # @classproperty
        # def river(_self):
        #     return RiverObject(_self)

        self.field_name = name

        # 添加 transition_approval 类
        self._add_to_class(cls, self.field_name + "_transition_approvals",
                           GenericRelation('%s.%s' % (TransitionApproval._meta.app_label, TransitionApproval._meta.object_name)))
        # 添加 transition 类
        self._add_to_class(cls, self.field_name + "_transitions", GenericRelation('%s.%s' %
                                                                                  (Transition._meta.app_label, Transition._meta.object_name)))

        # if id(cls) not in workflow_registry.workflows:
        #     self._add_to_class(cls, "river", river)

        super().contribute_to_class(cls, name, *args, **kwargs)

        # if id(cls) not in workflow_registry.workflows:
        #     post_save.connect(_on_workflow_object_saved, self.model, False,
        #                       dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))
        #     post_delete.connect(_on_workflow_object_deleted, self.model, False,
        #                         dispatch_uid='%s_%s_riverstatefield_post' % (self.model, name))

        workflow_registry.add(self.field_name, cls)

    @staticmethod
    def _add_to_class(cls, key, value, ignore_exists=False):
        if ignore_exists or not hasattr(cls, key):
            cls.add_to_class(key, value)


# def _on_workflow_object_saved(sender, instance, created, *args, **kwargs):
#     for instance_workflow in instance.river.all(instance.__class__):
#         if created:
#             # 初始化工作流
#             instance_workflow.initialize_approvals()
#             if not instance_workflow.get_state():
#                 # 设置初始状态
#                 init_state = getattr(instance.__class__.river, instance_workflow.field_name).initial_state
#                 instance_workflow.set_state(init_state)
#                 instance.save()


# def _on_workflow_object_deleted(sender, instance, *args, **kwargs):
#     pass
#     # OnApprovedHook.objects.filter(
#     #     object_id=instance.pk, content_type=ContentType.objects.get_for_model(instance.__class__)).delete()
#     # OnTransitHook.objects.filter(
#     #     object_id=instance.pk, content_type=ContentType.objects.get_for_model(instance.__class__)).delete()
#     # OnCompleteHook.objects.filter(
#     #     object_id=instance.pk, content_type=ContentType.objects.get_for_model(instance.__class__)).delete()
