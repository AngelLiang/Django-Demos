from django.contrib import admin

from .workflow import WorkflowAdmin
from .workflow_instance import WorkflowInstanceAdmin
from .state import StateAdmin
from .transitionapprovalmeta import TransitionApprovalMetaAdmin
from .transitionapproval import TransitionApprovalAdmin
from .transitionmeta import TransitionMetaAdmin
from .transition import TransitionAdmin
from .wforder import WforderAdmin

from .. import models

admin.site.register(models.Workflow, WorkflowAdmin)
admin.site.register(models.WorkflowInstance, WorkflowInstanceAdmin)
admin.site.register(models.State, StateAdmin)
admin.site.register(models.TransitionApprovalMeta, TransitionApprovalMetaAdmin)
admin.site.register(models.TransitionApproval, TransitionApprovalAdmin)
admin.site.register(models.TransitionMeta, TransitionMetaAdmin)
admin.site.register(models.Transition, TransitionAdmin)
admin.site.register(models.Wforder, WforderAdmin)
