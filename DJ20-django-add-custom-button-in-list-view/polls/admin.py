from django.contrib import admin
from django.urls import re_path, reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from .models import Question


class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'question_text',
        'pub_date',
        'status',
        'extra_buttons'
    )

    def get_urls(self):
        urls = super().get_urls()

        opts = self.model._meta
        app_label = opts.app_label
        model_name = opts.model_name

        custom_urls = [
            re_path(
                r'^(?P<object_id>.+)/publish/$',
                self.admin_site.admin_view(self.publish_confirm),
                name=f'{app_label}_{model_name}_publish',
            ),
        ]
        return custom_urls + urls

    ################################################################
    # 添加下面语句

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def extra_buttons(self, obj):
        html = ''
        params = []

        opts = self.model._meta
        app_label = opts.app_label
        model_name = opts.model_name

        if self.has_change_permission(self.request, obj):
            html += '<a class="button" href="{}">编辑</a>'
            params.append(reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk]))

        if self.has_delete_permission(self.request, obj):
            html += '&nbsp;' + '<a class="button" style="background:#CC3434;" href="{}">删除</a>'
            params.append(reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk]))

        if obj.status == obj.DRAFT:
            path = self.request.path
            html += '&nbsp;' + '<a class="button" href="{}">发布</a>'
            params.append(reverse(f'admin:{app_label}_{model_name}_publish', args=[obj.pk]) + f'?next={path}')

        return format_html(html, *params)

    extra_buttons.short_description = '操作'
    extra_buttons.allow_tags = True

    ################################################################

    def publish_confirm(self, request, object_id, *args, **kwargs):
        obj = self.get_object(request, object_id)

        opts = self.model._meta
        app_label = opts.app_label
        model_name = opts.model_name

        if request.POST.get('post'):
            try:
                obj.status = obj.PUBLISHED
                obj.save()
                self.message_user(request, _('发布成功'))
            except Exception as e:
                self.message_user(request, e)

            next = request.GET.get('next') or reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
            return HttpResponseRedirect(next)

        title = _("Are you sure?")
        objects_name = str(opts.verbose_name)
        action_name = '发布'

        context = dict(
            self.admin_site.each_context(request),
            title=title,
            opts=opts,
            objects_name=objects_name,
            object=obj,
            action_name=action_name,
        )

        # model_name = opts.model_name
        return TemplateResponse(request, f'admin/question/publish_confirm.html', context)


admin.site.register(Question, QuestionAdmin)
