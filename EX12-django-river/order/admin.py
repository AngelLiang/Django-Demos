from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

import river_admin

from . import models


def create_river_button(obj, transition_approval):
    """创建river按钮"""
    approve_order_url = reverse('approve_order', kwargs={
        'order_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return f"""
        <input
            type="button"
            style="margin:2px;2px;2px;2px;"
            value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
            onclick="location.href=\'{approve_order_url}\'"
        />
    """


class OrderItemInline(admin.TabularInline):
    """
    admin.TabularInline: 平行的表格
    admin.StackedInline: 垂直的表格

    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-options
    """
    model = models.OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('sn', 'status', 'created_at', 'river_actions')
    readonly_fields = ('sn',)

    list_filter = ('status',)

    inlines = [
        OrderItemInline
    ]

    def get_list_display(self, request):
        self.user = request.user  # 获取当前用户
        return super().get_list_display(request)

    def river_actions(self, obj):
        content = ""
        # print(f'{self.user} {self.user.groups.all()}')
        print(obj.river.status.on_final_state)
        # 遍历
        for transition_approval in obj.river.status.get_available_approvals(as_user=self.user):
            content += create_river_button(obj, transition_approval)

        return mark_safe(content)
    # river_actions.description = '状态操作'


admin.site.register(models.Product)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)


# class OrderRiverAdmin(river_admin.RiverAdmin):
#     name = "Issue Tracking Flow"
#     icon = "mdi-ticket-account"
#     list_displays = ['sn', 'status']


# river_admin.site.register(models.Order, 'status', OrderRiverAdmin)
