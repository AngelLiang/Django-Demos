import logging
from django.conf import settings
from django.contrib.auth.models import Permission, Group

from django.db import models
from django.db import transaction
from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


LOGGER = logging.getLogger(__name__)


class TransitionApprovalMeta(BaseModel):
    """流转批准元数据"""

    name = models.CharField(_('名称'), max_length=80, default='', blank=True)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)

    # 工作流
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.PROTECT,
        related_name='transition_approval_metas',
    )

    # 流转元数据
    transition_meta = models.ForeignKey(
        'TransitionMeta',
        verbose_name=_('流转元数据'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_approval_meta',
    )

    priority = models.IntegerField(_('优先级'), default=0, null=True, blank=True)
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    # 父级 多对多
    parents = models.ManyToManyField(
        'self', verbose_name=_('父级'),
        symmetrical=False,
        db_constraint=False,
        db_index=True,
        blank=True,
        related_name='children',
    )

    ################################################################
    # 通知字段
    ################################################################
    # 邮件通知
    email_notice = models.BooleanField(_('邮件通知'), default=False)
    # 短信通知
    short_message_notice = models.BooleanField(_('短信通知'), default=False)
    # 微信通知
    weixin_notice = models.BooleanField(_('微信通知'), default=False)

    ################################################################
    # 指定处理人字段
    ################################################################

    # 处理类型
    HT_DESIGNATED_USERS = 'users'
    HT_DESIGNATED_POSITIONS = 'positions'
    HT_DESIGNATED_ROLES = 'roles'
    HT_DESIGNATED_UNITS = 'units'
    HT_SUBBMITER = 'subbmiter'
    HT_CUSTOM_FUNCTION = 'custom_function'
    HT_CUSTOM_SQL = 'custom_sql'

    HT_CHOICES = (
        (HT_DESIGNATED_USERS, _('指定用户')),  # 指定用户
        (HT_DESIGNATED_POSITIONS, _('指定岗位')),  # 指定岗位
        (HT_DESIGNATED_ROLES, _('指定角色')),  # 指定角色
        (HT_DESIGNATED_UNITS, _('指定部门')),  # 指定部门
        (HT_SUBBMITER, _('提交人')),    # 提交人
        (HT_CUSTOM_FUNCTION, _('自定义审批处理类')),
        (HT_CUSTOM_SQL, _('自定义SQL处理人')),
    )
    HT_DEFAULT = HT_SUBBMITER
    # 处理类型
    handler_type = models.CharField(
        _('审批处理类型'),
        max_length=40,
        choices=HT_CHOICES,
        default=HT_DEFAULT,
    )

    # 岗位 多对多
    positions = models.ManyToManyField(
        'hr.Position',
        verbose_name=_('指定岗位'),
        db_constraint=False,
        blank=True
    )
    # 角色 多对多
    roles = models.ManyToManyField(
        'customauth.Role',
        verbose_name=_('指定角色'),
        db_constraint=False,
        blank=True
    )
    # 用户 多对多
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('指定用户'),
        db_constraint=False,
        blank=True,
        related_name='+'
    )
    # 部门单元 多对多
    orgunits = models.ManyToManyField(
        'organization.OrgUnit',
        verbose_name=_('指定部门单元'),
        db_constraint=False,
        blank=True
    )

    NUH_CHOICES = (
        ('ParentPosition', _('提交人的上级')),
    )
    user_handler_function = models.CharField(
        _('next用户处理类'),
        max_length=80,
        blank=True, null=True,
        choices=NUH_CHOICES,
    )

    # 自定义处理人SQL
    user_handler_sql = models.TextField(
        _('处理人SQL'),
        blank=True, null=True,
        # help_text=u'自定义SQL语句，优先高于指定用户、岗位、角色'
    )

    ################################################################

    def __str__(self):
        return '流转: %s, 优先级: %s' % (self.transition_meta, self.priority)

    class Meta:
        verbose_name = _('批准元数据')
        verbose_name_plural = _('批准元数据')
        unique_together = [('workflow', 'transition_meta', 'priority')]

    @property
    def peers(self):
        return TransitionApprovalMeta.objects.filter(
            workflow=self.workflow,
            # transition_meta=self.transition_meta,
        ).exclude(pk=self.pk)

    def get_users_from_handler_type(self, request, obj):
        """通过处理类型获取处理用户"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        tp = self.handler_type
        if tp == self.HT_DESIGNATED_USERS and self.users:
            # 用户
            users = [user for user in self.users.all()]
            return users
        elif tp == self.HT_DESIGNATED_POSITIONS and self.positions:
            # 岗位
            # users = []
            # for position in self.positions.all():
            #     for employee in position.employee_set.all():
            #         if employee.user:
            #             users.append(employee.user)

            # positions = self.positions.all()
            # users = User.objects.filter(employee__position__in=positions).all()

            positions_ids = self.positions.values_list('id', flat=True)
            LOGGER.debug(f'positions_ids:{positions_ids}')
            users = User.objects.filter(employee__position__id__in=positions_ids).all()
            LOGGER.debug(f'users:{users}')
            return users
        elif tp == self.HT_DESIGNATED_ROLES and self.roles:
            # 角色
            users = []
            for role in self.roles.all():
                for user in role.users.all():
                    users.append(user)
            return users
        elif tp == self.HT_DESIGNATED_UNITS and self.orgunits:
            # 部门
            users = []
            for unit in self.orgunits.all():
                for position in unit.positions.all():
                    for employee in position.employee_set.all():
                        if employee.user:
                            users.append(employee.user)
        elif tp == self.HT_SUBBMITER:
            # 申请人
            return [obj.user]
        elif tp == self.HT_CUSTOM_FUNCTION and self.user_handler_function:
            # 自定义处理函数
            from rworkflow.handlers.wfusers import wfusers_mapping
            handler_func = wfusers_mapping.get(self.user_handler_function)
            if handler_func:
                return handler_func(request, obj, self)
        elif tp == self.HT_CUSTOM_SQL and self.user_handler_sql:
            # 自定义SQL
            handler = self.user_handler_sql
            if handler:
                handler = handler.replace(
                    "submitter()", obj.user.username)  # 提交人
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

        return []

    def get_handle_users(self):
        return []


def post_save_model(sender, instance, *args, **kwargs):
    parents = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, transition_meta__destination_state=instance.transition_meta.source_state) \
        .exclude(pk__in=instance.parents.values_list('pk', flat=True)) \
        .exclude(pk=instance.pk)

    children = TransitionApprovalMeta.objects \
        .filter(workflow=instance.workflow, transition_meta__source_state=instance.transition_meta.destination_state) \
        .exclude(parents__in=[instance.pk]) \
        .exclude(pk=instance.pk)

    instance = TransitionApprovalMeta.objects.get(pk=instance.pk)
    if parents:
        instance.parents.add(*parents)

    for child in children:
        child.parents.add(instance)

    # 有 parents 表示 source_state 非起始节点
    if instance.parents.count() == 0:
        instance.transition_meta.source_state.is_start = True
    else:
        instance.transition_meta.source_state.is_start = False
    instance.transition_meta.source_state.save(update_fields=['is_start'])

    # 有 children 表示 destination_state 非终止节点
    if instance.children.count() == 0:
        instance.transition_meta.destination_state.is_stop = True
    else:
        instance.transition_meta.destination_state.is_stop = False
    instance.transition_meta.destination_state.save(update_fields=['is_stop'])


@transaction.atomic
def pre_delete_model(sender, instance, *args, **kwargs):
    from .transitionapproval import TransitionApproval
    # 删除所有 PENDING 状态 的 transition_approval
    instance.transition_approvals.filter(status=TransitionApproval.PENDING).delete()


post_save.connect(post_save_model, sender=TransitionApprovalMeta)
pre_delete.connect(pre_delete_model, sender=TransitionApprovalMeta)
