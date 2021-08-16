from django.contrib import admin
from django.shortcuts import get_object_or_404
from ..tables import TransitionApprovalTable
from river.models import TransitionApproval


class RiverAdminMixin(admin.ModelAdmin):

    def get_object_history_template(self):
        template_list = [
            "admin/%s/%s/object_history.html" % (self.opts.app_label, self.opts.model_name),
            "admin/%s/object_history.html" % self.opts.app_label,
            'admin/river_patch/object_history.html',
            "admin/object_history.html",
        ]
        return template_list
    object_history_template = property(get_object_history_template)

    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        # 获取对象
        obj = self.get_object(request, object_id)
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, self.opts, object_id)

        approvals = TransitionApproval.objects.filter(
            workflow_object=obj,
        ).filter(transaction_date__isnull=False).order_by('-transaction_date')

        approvals_table = TransitionApprovalTable(approvals)
        approvals_table.paginate(page=request.GET.get('page', 1), per_page=25)
        extra_context.update({
            'approvals': approvals,
            'approvals_table': approvals_table,
        })

        return super().history_view(request, object_id, extra_context)
