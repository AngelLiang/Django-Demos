from django.conf import settings
from django.contrib.auth.models import Permission, Group

from django.db import models, transaction
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


class TransitionApprovalMeta(BaseModel):
    """流转批准元数据"""

    # 工作流
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流'),
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

    # 权限
    permissions = models.ManyToManyField(Permission, verbose_name=_('权限'), blank=True)
    # 权限组
    groups = models.ManyToManyField(Group, verbose_name=_('权限组'), blank=True)

    priority = models.IntegerField(_('排序'), default=0, null=True, blank=True)

    # 父级 多对多
    parents = models.ManyToManyField(
        'self', verbose_name=_('父级'),
        symmetrical=False, db_index=True, blank=True,
        related_name='children',
    )

    ################################################################
    # 指定处理人字段
    ################################################################

    handler = models.TextField(
        _('处理人SQL'),
        blank=True, null=True,
        # help_text=u'自定义SQL语句，优先高于指定用户、岗位、角色'
    )

    NUH_CHOICES = (
        ('ParentPosition', _('提交人的上级')),
    )
    next_user_handler = models.CharField(
        _('next用户处理类'),
        max_length=80,
        blank=True, null=True,
        choices=NUH_CHOICES,
    )

    # 处理类型
    HT_DESIGNATED_USERS = '00'
    HT_DESIGNATED_POSITIONS = '10'
    HT_DESIGNATED_ROLES = '20'
    HT_SUBBMITER = '90'
    HT_CHOICES = (
        (HT_DESIGNATED_USERS, _('指定用户')),  # 指定用户
        # (HT_DESIGNATED_POSITIONS, _('指定岗位')),  # 指定岗位
        # (HT_DESIGNATED_ROLES, _('指定角色')),  # 指定角色
        (HT_SUBBMITER, _('提交人')),    # 提交人
    )
    HT_DEFAULT = HT_DESIGNATED_USERS
    # 处理类型
    handler_type = models.CharField(
        _('处理类型'),
        max_length=16,
        choices=HT_CHOICES,
        default=HT_DEFAULT,
    )

    # 岗位 多对多
    # positions = models.ManyToManyField('hr.Position', verbose_name=_('指定岗位'), blank=True)
    # 角色 多对多
    # roles = models.ManyToManyField('account.Role', verbose_name=_('指定角色'), blank=True)
    # 用户 多对多
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('指定用户'), blank=True)
    # 部门单元 多对多
    # orgunits = models.ManyToManyField('organization.OrgUnit', verbose_name=_('指定部门单元'), blank=True)

    ################################################################
    # 通知字段
    ################################################################
    # 邮件通知
    email_notice = models.BooleanField(_('邮件通知'), default=True)
    # 短信通知
    short_message_notice = models.BooleanField(_('短信通知'), default=False)
    # 微信通知
    weixin_notice = models.BooleanField(_('微信通知'), default=False)

    def __str__(self):
        return '流转: %s, 排序: %s' % (self.transition_meta, self.priority)

    class Meta:
        verbose_name = _('流转批准元数据')
        verbose_name_plural = _('流转批准元数据')
        # unique_together = [('workflow', 'transition_meta', 'priority')]

    def can_handle(self, request):
        user = request.user

        tp = self.handler_type
        if tp == self.HT_DESIGNATED_USERS and self.users:
            user = self.users.filter(id=user.id).first()
            if user:
                return True
        elif tp == self.HT_SUBBMITER:
            pass

        return qs

    # def filter_handle_users(self, qs):
    #     pass

    def get_users_from_handler_type(self, request):
        tp = self.handler_type
        if tp == self.HT_DESIGNATED_USERS and self.users:
            # user
            users = [user for user in self.users.all()]
            return users
        # elif tp == self.HT_DESIGNATED_POSITIONS and self.positions:
        #     # position
        #     users = []
        #     for position in self.positions.all():
        #         for employee in position.employee_set.all():
        #             users.append(employee.user)
        #     return users
        # elif tp == self.HT_DESIGNATED_ROLES and self.roles:
        #     # role
        #     users = []
        #     for role in self.roles.all():
        #         for user in role.users.all():
        #             users.append(user)
        #     return users
        elif tp == self.HT_SUBBMITER:
            # submitter
            return [request.user]
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


@transaction.atomic
def pre_delete_model(sender, instance, *args, **kwargs):
    from .transitionapproval import TransitionApproval
    PENDING = TransitionApproval.PENDING
    # 删除所有 PENDING 的 transition_approval
    instance.transition_approvals.filter(status=PENDING).delete()


post_save.connect(post_save_model, sender=TransitionApprovalMeta)
pre_delete.connect(pre_delete_model, sender=TransitionApprovalMeta)
