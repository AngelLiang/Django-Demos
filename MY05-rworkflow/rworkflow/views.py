import datetime as dt

from django.db import connection
from django.contrib.admin import site
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


from . import models

SELECTED_CHECKBOX_NAME = 'NEXT_NODE_USER'


def compile_node_handler(request, obj, next_node):
    """ 获取下一节点的处理者

    :param request:
    :param obj:
    :param next_node:

    :return:
    """

    # 下一个用户处理类
    next_user_handler = next_node.next_user_handler
    # next_user_handler 具有最高优先级
    if next_user_handler:
        handler_func = wfusers_mapping.get(next_user_handler)
        if handler_func:
            return handler_func(request, obj, next_node)

    # 获取自定义 SQL 语句
    handler = next_node.handler
    if handler and handler != '':
        handler = handler.replace("submitter()", request.user.username)
        handler = handler.replace("suber()", request.user.username)
        fields = obj._meta.fields
        for field in fields:
            name = field.name
            temp = f"{{name}}"
            val = getattr(obj, name, None)
            if val:
                if not isinstance(val, str):
                    val = str(val)
                handler = handler.replace(temp, val)
        cursor = connection.cursor()
        cursor.execute(handler)
        rows = [row for row in cursor.fetchall()]
        return rows
    # 根据 handler_type 返回对应的用户
    return next_node.get_users_from_handler_type(request)


def wf_start(request, app, model, object_id):
    """启动工作流"""

    content_type = ContentType.objects.get(app_label=app, model=model)
    obj = content_type.get_object_for_this_type(id=int(object_id))
    title = _("Are you sure?")
    opts = obj._meta
    objects_name = opts.verbose_name

    # 定义变量
    has_workflow = False
    workflow = None
    next_node = None
    next_users = []
    has_next_user = False

    # 获取工作流
    queryset = models.Workflow.objects.filter(content_type=content_type)
    cnt = queryset.count()

    if cnt > 0:
        has_workflow = True
        workflow = queryset.first()
        # 起始节点
        query_start_node = workflow.states.filter(is_start=True)
        # 第一个节点
        query_first_node = workflow.states.order_by('id')

        if query_start_node.count() > 0:
            # 起始节点大于零
            next_node = query_start_node[0]
        elif query_first_node.count() > 0:
            next_node = query_first_node[0]

        if next_node:
            # 获取下一节点的处理用户
            next_users = compile_node_handler(request, obj, next_node)
            if len(next_users) > 0:
                has_next_user = True
    else:
        title = _('没有配置工作流')

    # 获取工作流实例，判断该对象是否处于工作流中
    try:
        tmp = models.WorkflowInstance.objects.get(workflow=workflow, object_id=object_id)
        messages.warning(request, _('该实例已经处于工作流程中了'))
        return HttpResponseRedirect("/admin/%s/%s/%s" % (app, model, object_id))
    except Exception:
        pass

    if request.POST.get("post"):
        val = request.POST.getlist(SELECTED_CHECKBOX_NAME)

        # 创建实例
        workflow_inst, is_created = models.WorkflowInstance.objects.get_or_create(
            workflow=workflow, object_id=object_id, starter=request.user
        )
        workflow_inst.current_nodes.add(next_node)
        workflow_inst.save()

        # 工作流审批记录
        workflow_history = models.WorkflowHistory.objects.create(instance=workflow_inst, user=request.user)

        # 创建代办事项
        for user in User.objects.filter(id__in=val):
            todo = models.TodoList.objects.create(
                instance=workflow_inst, user=user,
                app_label=app, model_name=model,
                node=next_node,
            )
        todo = models.TodoList.objects.create(
            instance=workflow_inst, user=request.user,
            app_label=app, model_name=model,
            is_read=True, read_at=dt.datetime.now(),
            is_done=True
        )

        # 设置工作流中那个模型的状态
        if next_node.status_field and next_node.status_value:
            try:
                setattr(obj, next_node.status_field, next_node.status_value)
                obj.save(update_fields=[next_node.status_field])
            except Exception:
                pass
        messages.success(request, _('审批流程成功启动'))
        return HttpResponseRedirect("/admin/%s/%s/%s" % (app, model, object_id))

    context = dict(
        site.each_context(request),
        title=title,
        opts=opts,
        objects_name=objects_name,
        object=obj,
        has_workflow=has_workflow,
        workflow_modal=workflow,
        next_node=next_node,
        has_next_user=has_next_user,
        next_users=next_users,
        checkbox_name=SELECTED_CHECKBOX_NAME,
    )
    request.current_app = site.name

    return TemplateResponse(request, 'admin/workflow/workflow_start_confirmation.html', context)


from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import State, Wforder


def approve_order(request, order_id, next_state_id=None):
    order = get_object_or_404(Wforder, pk=order_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        # order.river.status.approve(as_user=request.user, next_state=next_state)
        # admin:<app>_<model>_changelist
        return redirect(reverse('admin:rworkflow_wforder_changelist'))
    except Exception as e:
        return HttpResponse(e.message)
