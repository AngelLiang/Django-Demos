from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import path
from django.urls import reverse
from django.utils.safestring import mark_safe
from river.models import TransitionApproval
from river.models import State

from ..tables import TransitionApprovalTable



class RiverAdminMixin(admin.ModelAdmin):

    def get_list_display(self, request):
        self._current_uesr = request.user  # 获取当前用户
        return super().get_list_display(request)

    def river_approve_view(self, request, object_id, next_state_id=None):
        obj = self.get_object(request, object_id)
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, self.opts, object_id)

        next_state = get_object_or_404(State, pk=next_state_id)

        try:
            obj.river.status.approve(as_user=request.user, next_state=next_state)
            # admin:<app>_<model>_changelist
            return redirect(reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_changelist'))
        except Exception as e:
            return HttpResponse(e)

    def get_urls(self):
        urls = super().get_urls()
        return [
            path('<int:object_id>/river/approve/<int:next_state_id>/',
                 self.river_approve_view,
                 name=f'{self.opts.app_label}_{self.opts.model_name}_river_approve_view'),
        ] + urls


    def create_river_button(self, obj, transition_approval):
        """创建river按钮"""
        approve_url = reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_river_approve_view', kwargs={
                                    'object_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
        return f"""
            <input
                type="button"
                style="margin:2px;2px;2px;2px;"
                value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
                onclick="location.href=\'{approve_url}\'"
            />
        """

    def river_actions(self, obj):
        content = ""
        # 遍历
        for transition_approval in obj.river.status.get_available_approvals(as_user=self._current_uesr):
            content += self.create_river_button(obj, transition_approval)

        return mark_safe(content)


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
