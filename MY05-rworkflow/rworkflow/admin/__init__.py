from django.contrib import admin
from django.utils.text import capfirst
from collections import OrderedDict as SortedDict

from .workflow import WorkflowAdmin
from .workflow_category import WorkflowCategoryAdmin
from .workflow_instance import WorkflowInstanceAdmin
from .state import StateAdmin
from .transitionapprovalmeta import TransitionApprovalMetaAdmin
from .transitionapproval import TransitionApprovalAdmin
from .transitionmeta import TransitionMetaAdmin
from .transition import TransitionAdmin
from .wforder import WforderAdmin
from .extraparam import ExtraParamMetaAdmin, ExtraParamAdmin


from .. import models


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        for app in template_response.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return template_response
    return inner


registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

admin.site.register(models.Wforder, WforderAdmin)
admin.site.register(models.Workflow, WorkflowAdmin)
admin.site.register(models.WorkflowCategory, WorkflowCategoryAdmin)
admin.site.register(models.WorkflowInstance, WorkflowInstanceAdmin)
admin.site.register(models.State, StateAdmin)
admin.site.register(models.TransitionApproval, TransitionApprovalAdmin)
admin.site.register(models.TransitionApprovalMeta, TransitionApprovalMetaAdmin)
admin.site.register(models.Transition, TransitionAdmin)
admin.site.register(models.TransitionMeta, TransitionMetaAdmin)
admin.site.register(models.ExtraParam, ExtraParamAdmin)
admin.site.register(models.ExtraParamMeta, ExtraParamMetaAdmin)
