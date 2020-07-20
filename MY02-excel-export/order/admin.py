import xlwt
from io import BytesIO

from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from . import models
from .excelutils import (
    get_noraml_style, get_label_style, get_headers_style
)


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ('product', 'quantity', 'price', 'amount',)
    readonly_fields = ('amount',)
    extra = 0

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_code()

    def get_urls(self):
        opts = self.opts
        urls = super().get_urls()
        return [
            url(r'(?P<obj_id>\d+)/excel-export', self.detail_export_action,
                name=f'{opts.app_label}_{opts.model_name}_detailexport'),
        ] + urls

    def has_detail_export_permission(self, request):
        user = request.user
        # permission_code = 'get_detail_excel'
        permission_code = getattr(settings, 'DETAIL_EXPORT_PERMISSION_CODE', None)
        if permission_code is None:
            return True

        opts = self.opts
        codename = f'{permission_code}_{opts.model_name}'
        return user.has_perm(f'{opts.app_label}.{codename}')

    def detail_export_action(self, request, obj_id):

        # 判断权限
        if not self.has_detail_export_permission(request):
            raise PermissionDenied

        obj = self.get_object(request, obj_id)
        if obj is None:
            opts = self.opts
            return self._get_obj_does_not_exist_redirect(request, opts, obj_id)

        style = get_noraml_style()
        lstyle = get_label_style()
        hstyle = get_headers_style()

        headers = ('物料', '单价', '数量', '小计',)
        width = len(headers)

        row = 0
        row2_left = len(headers) // 2
        row_right = width - 1

        ws = xlwt.Workbook(encoding='utf8')
        sheet = ws.add_sheet('sheet1')

        # 标题
        sheet.write_merge(row, 0, row, row_right, str(obj.title), hstyle)

        row += 1
        sheet.write_merge(row, row, 0, 0, '订单号', lstyle)
        sheet.write_merge(row, row, 1, row2_left - 1, str(obj.code), style)
        sheet.write_merge(row, row, row2_left, row2_left, '客户', lstyle)
        sheet.write_merge(row, row, row2_left + 1, row_right, obj.customer.name, style)

        row += 1
        sheet.write_merge(row, row, 0, 0, '订单日期', lstyle)
        sheet.write_merge(row, row, 1, row2_left - 1, str(obj.order_date), style)
        sheet.write_merge(row, row, row2_left, row2_left, '创建时间', lstyle)
        sheet.write_merge(row, row, row2_left + 1, row_right, str(obj.created_at), style)

        row += 1
        sheet.write_merge(row, row, 0, 0, '总金额', lstyle)
        sheet.write_merge(row, row, 1, row2_left - 1, obj.amount, style)
        # sheet.write_merge(row, row, row2_left, row2_left, '折扣金额', lstyle)
        # sheet.write_merge(row, row, row2_left + 1, row_right, obj.discount_amount, style)

        row += 1
        sheet.write_merge(row, row + 2, 0, 0, '描述信息', lstyle)
        sheet.write_merge(row, row + 2, 1, width - 1, obj.description, style)

        ########################################################
        # 明细行

        row += 3
        sheet.write_merge(row, row, 0, width - 1, '订单明细', hstyle)
        row += 1
        for i, header in enumerate(headers):
            sheet.write(row, i, header, hstyle)

        items = obj.items.all()
        row += 1
        first_col_max_width = 4
        for item in items:
            data = (
                item.product.name, item.price, item.quantity, item.amount,
            )
            name_len = len(item.product.name)
            if name_len > first_col_max_width:
                first_col_max_width = name_len
            for i, dat in enumerate(data):
                sheet.write(row, i, dat, style)
            row += 1

        # xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位。
        # xlwt创建时使用的默认宽度为2960，即11个字符0的宽度
        first_col = sheet.col(0)
        first_col.width = 256 * first_col_max_width * 2    # 256为衡量单位

        ########################################################

        bio = BytesIO()
        ws.save(bio)
        bio.seek(0)
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={obj.code}.xls'
        # response.write(bio.getvalue())
        return response


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
