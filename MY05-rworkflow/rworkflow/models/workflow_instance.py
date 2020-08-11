import logging
from decimal import Decimal

import six
from django.db import models
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Max
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# from DjangoUeditor.models import UEditorField

# from common import const
from .base import BaseModel
from .transition import Transition
from .transitionapproval import TransitionApproval
from .state import State

LOGGER = logging.getLogger(__name__)


class WorkflowInstance(BaseModel):
    """工作流实例"""

    code = models.CharField(_('编号'), max_length=80, null=True, blank=True)

    # 关联的工作流模型
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('关联的工作流模型'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='instances',
    )

    ################################################################
    # 关联的对象
    ################################################################
    # content_type = models.ForeignKey(
    #     ContentType,
    #     verbose_name=_('内容类型'),
    #     on_delete=models.PROTECT,
    #     db_constraint=False,
    # )
    object_id = models.PositiveIntegerField(_('对象ID'), blank=True, null=True)
    # workflow_object = GenericForeignKey('content_type', 'object_id')

    # 发起人
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('发起人'),
        on_delete=models.PROTECT,
        related_name='+',
    )
    # 发起时间
    start_at = models.DateTimeField(_('发起时间'), auto_now_add=True)
    # 批准时间
    # approved_at = models.DateTimeField(_('批准时间'), blank=True, null=True)

    # # STATUS_CHOICES = (
    # #     ('00', _("NEW")),          # 新建
    # #     ('10', _("IN PROGRESS")),  # 在处理
    # #     ('20', _("DENY")),         # 拒绝
    # #     ('40', _("TERMINATED")),   # 终止
    # #     ('80', _("APPROVED")),     # 批准
    # #     ('90', _("COMPLETED"))     # 结束
    # # )
    # STATUS_INPROGRESS = '10'
    # STATUS_DENY = '20'

    # STATUS_CHOICES = const.get_value_list('S072')
    # STATUS_CHOICES_MAPPING = dict(const.get_value_list('S072') or {})
    # STATUS_DEFAULT = const.get_default_value('S072')
    # STATUS_QUERYSET = const.get_value_queryset('S072')
    # # 状态
    # status = models.CharField(_('状态'), max_length=const.DB_STATUS_LENGTH)

    # # 当前节点 多对多
    # current_nodes = models.ManyToManyField('Node', verbose_name=_('当前节点'), blank=True)

    initialized = models.BooleanField(_('已初始化？'), default=False)

    def __str__(self):
        return f'{self.code}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.code:
            self.code = 'WFI%05d' % self.id
            self.save(update_fields=['code'])

    class Meta:
        verbose_name = _('流程实例')
        verbose_name_plural = _('流程实例')
        default_permissions = ('view',)

    def get_content_type(self):
        app_label = self.workflow.app_label
        model_name = self.workflow.model_name
        return ContentType.objects.get(app_label=app_label, model=model_name)

    def get_object_id(self):
        return self.object_id

    def get_workflow_object(self):
        if hasattr(self, '_workflow_object'):
            return self._workflow_object
        content_type = self.get_content_type()
        object_id = self.get_object_id()
        obj = content_type.get_object_for_this_type(id=int(object_id))
        self._workflow_object = obj
        return obj
    workflow_object = property(get_workflow_object)

    # @property
    # def workflow_object(self):
    #     self.get_workflow_object()
    #     return obj

    @transaction.atomic
    def initialize_approvals(self, request):
        """初始化批准流程"""

        if not self.initialized:
            object_id = self.get_object_id()
            content_type = self.get_content_type()
            workflow_object = self.get_workflow_object()

            # if self.workflow and self.workflow.transition_approvals.filter(workflow_object=workflow_object).count() == 0:
            if self.workflow and self.workflow.transition_approvals.filter(
                object_id=object_id, content_type=content_type
            ).count() == 0:
                # 获取工作流流转元数据
                # transition_meta_list = self.workflow.transition_metas.filter(source_state=self.workflow.initial_state)

                # 获取所有初始流转元数据
                transition_meta_list = self.workflow.transition_metas.filter(source_state__is_start=True)
                LOGGER.debug(transition_meta_list)

                # 迭代次数
                iteration = 0
                # 已经处理过的 transitions
                processed_transitions = []
                while transition_meta_list:
                    for transition_meta in transition_meta_list:
                        # 通过 transition_meta 创建 transition
                        transition = Transition.objects.create(
                            workflow=self.workflow,
                            workflow_object=workflow_object,
                            source_state=transition_meta.source_state,
                            destination_state=transition_meta.destination_state,
                            meta=transition_meta,
                            iteration=iteration
                        )
                        # 通过 transition_approval_meta 创建 transition_approval
                        for transition_approval_meta in transition_meta.transition_approval_meta.all():

                            transition_approval = TransitionApproval.objects.create(
                                workflow=self.workflow,
                                workflow_object=workflow_object,
                                transition=transition,
                                priority=transition_approval_meta.priority,
                                can_edit=transition_approval_meta.can_edit,
                                can_take=transition_approval_meta.can_take,
                                meta=transition_approval_meta,
                            )
                            users = transition_approval_meta.get_users_from_handler_type(request, workflow_object)
                            LOGGER.debug(f'{users}')
                            if users:
                                transition_approval.users.add(*users)
                            # transition_approval.permissions.add(*transition_approval_meta.permissions.all())
                            # transition_approval.groups.add(*transition_approval_meta.groups.all())
                        processed_transitions.append(transition_meta.pk)
                    # 下一个 transition_meta 列表
                    transition_meta_list = self.workflow.transition_metas.filter(
                        source_state__in=transition_meta_list.values_list("destination_state", flat=True)
                    ).exclude(pk__in=processed_transitions)

                    iteration += 1
                # while end
                self.initialized = True
                self.save(update_fields=['initialized'])

                # 设置 workflow_object 初始状态
                init_state = self.workflow.states.filter(is_start=True).first()
                self.set_state(init_state)

                LOGGER.debug("Transition approvals are initialized for the workflow object %s" % self.workflow_object)

    @property
    def status_field(self):
        return self.workflow.status_field

    @property
    def on_initial_state(self):
        """处于初始状态"""
        # return self.get_state() == self.class_workflow.initial_state
        state = self.get_state()
        return state.is_start is True

    @property
    def on_final_state(self):
        """处于结束状态"""
        # return self.class_workflow.final_states.filter(pk=self.get_state().pk).count() > 0
        state = self.get_state()
        return state.is_stop is True

    def get_next_approvals(self):
        """获取下一个批准"""
        workflow_object = self.workflow_object
        state = self.get_state()
        transitions = Transition.objects.filter(
            workflow=self.workflow, object_id=workflow_object.pk, source_state=state
        )
        return TransitionApproval.objects.filter(transition__in=transitions)
    next_approvals = property(get_next_approvals)

    def get_current_approval(self):
        try:
            workflow_object = self.workflow_object
            TransitionApproval.objects.filter(
                workflow=self.workflow, object_id=workflow_object.pk
            ).filter(transaction_at__isnull=False).latest('transaction_at')
            # return getattr(self.workflow_object, self.field_name + "_transition_approvals").filter(transaction_at__isnull=False).latest('transaction_at')
        except TransitionApproval.DoesNotExist:
            return None
    recent_approval = property(get_current_approval)

    @transaction.atomic
    def jump_to(self, state):
        def _transitions_before(iteration):
            return Transition.objects.filter(workflow=self.workflow, workflow_object=self.workflow_object, iteration__lte=iteration)

        try:
            recent_iteration = self.recent_approval.transition.iteration if self.recent_approval else 0
            jumped_transition = getattr(self.workflow_object, self.field_name + "_transitions").filter(
                iteration__gte=recent_iteration, destination_state=state, status=Transition.PENDING
            ).earliest("iteration")

            jumped_transitions = _transitions_before(jumped_transition.iteration).filter(status=Transition.PENDING)
            for approval in TransitionApproval.objects.filter(pk__in=jumped_transitions.values_list("transition_approvals__pk", flat=True)):
                approval.status = TransitionApproval.JUMPED
                approval.save()
            jumped_transitions.update(status=Transition.JUMPED)
            self.set_state(state)
            self.workflow_object.save()

        except Transition.DoesNotExist:
            # raise RiverException(ErrorCode.STATE_IS_NOT_AVAILABLE_TO_BE_JUMPED,
            #                      "This state is not available to be jumped in the future of this object")
            ValueError("This state is not available to be jumped in the future of this object")

    def get_available_states(self, as_user=None):
        """获取可用的状态"""
        all_destination_state_ids = self.get_available_approvals(
            as_user=as_user).values_list('transition__destination_state', flat=True)
        return State.objects.filter(pk__in=all_destination_state_ids)

    def get_available_approvals(self, as_user=None, destination_state=None):
        """获取所有相关用户可用的批准流程"""
        # 需要重写
        # qs = self.class_workflow.get_available_approvals(as_user, ).filter(object_id=self.workflow_object.pk)

        qs = self.next_approvals
        qs = qs.filter(status=TransitionApproval.PENDING)
        if as_user:
            qs = qs.filter(users__id=as_user.id)

        if destination_state:
            qs = qs.filter(transition__destination_state=destination_state)

        return qs

    @transaction.atomic
    def approve(self, as_user, next_state=None):
        """批准"""
        available_approvals = self.get_available_approvals(as_user=as_user)
        number_of_available_approvals = available_approvals.count()
        if number_of_available_approvals == 0:
            # raise RiverException(ErrorCode.NO_AVAILABLE_NEXT_STATE_FOR_USER,
            #                      "There is no available approval for the user.")
            raise ValueError("There is no available approval for the user.")
        elif next_state:
            available_approvals = available_approvals.filter(transition__destination_state=next_state)
            if available_approvals.count() == 0:
                available_states = self.get_available_states(as_user)
                # raise RiverException(ErrorCode.INVALID_NEXT_STATE_FOR_USER, "Invalid state is given(%s). Valid states is(are) %s" % (
                #     next_state.__str__(), ','.join([ast.__str__() for ast in available_states])))
                raise ValueError()
        elif number_of_available_approvals > 1 and not next_state:
            # raise RiverException(ErrorCode.NEXT_STATE_IS_REQUIRED,
            #                      "State must be given when there are multiple states for destination")
            raise ValueError("State must be given when there are multiple states for destination")

        approval = available_approvals.first()
        approval.status = TransitionApproval.APPROVED
        approval.transactioner = as_user
        approval.transaction_at = timezone.now()
        approval.previous = self.recent_approval
        approval.save()

        if next_state:
            self.cancel_impossible_future(approval)

        has_transit = False
        if approval.peers.filter(status=TransitionApproval.PENDING).count() == 0:
            approval.transition.status = Transition.DONE
            approval.transition.save()
            previous_state = self.get_state()
            # 设置新的状态
            # LOGGER.debug(approval.transition.destination_state)
            self.set_state(approval.transition.destination_state)

            has_transit = True
            if self._check_if_it_cycled(approval.transition):
                self._re_create_cycled_path(approval.transition)
            LOGGER.debug("Workflow object '%s' is proceeded for next transition. Transition: %s -> %s" % (
                self.workflow_object, previous_state, self.get_state()))

        # with self._approve_signal(approval), self._transition_signal(has_transit, approval), self._on_complete_signal():
        #     self.workflow_object.save()

        workflow_object = self.workflow_object
        workflow_object.save()

    @transaction.atomic
    def cancel_impossible_future(self, approved_approval):
        transition = approved_approval.transition

        possible_transition_ids = {transition.pk}

        possible_next_states = {transition.destination_state.id}
        while possible_next_states:
            possible_transitions = Transition.objects.filter(
                workflow=self.workflow,
                object_id=self.workflow_object.pk,
                status=Transition.PENDING,
                source_state__id__in=possible_next_states
            ).exclude(pk__in=possible_transition_ids)

            possible_transition_ids.update(set(possible_transitions.values_list("pk", flat=True)))

            possible_next_states = set(possible_transitions.values_list("destination_state__id", flat=True))

        cancelled_transitions = Transition.objects.filter(
            workflow=self.workflow,
            object_id=self.workflow_object.pk,
            status=Transition.PENDING,
            iteration__gte=transition.iteration
        ).exclude(pk__in=possible_transition_ids)

        TransitionApproval.objects.filter(transition__in=cancelled_transitions).update(
            status=TransitionApproval.CANCELLED)
        cancelled_transitions.update(status=TransitionApproval.CANCELLED)

    def _check_if_it_cycled(self, done_transition):
        qs = Transition.objects.filter(
            workflow_object=self.workflow_object,
            workflow=self.workflow,
            source_state=done_transition.destination_state
        )

        return qs.filter(status=Transition.DONE).count() > 0 and qs.filter(status=Transition.PENDING).count() == 0

    def _get_transition_images(self, source_states):
        meta_max_iteration = Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state__pk__in=source_states,
        ).values_list("meta").annotate(max_iteration=Max("iteration"))

        return Transition.objects.filter(
            Q(workflow=self.workflow, object_id=self.workflow_object.pk)
            & six.moves.reduce(lambda agg, q: q | agg, [Q(meta__id=meta_id, iteration=max_iteration) for meta_id, max_iteration in meta_max_iteration], Q(pk=-1))
        )

    def _re_create_cycled_path(self, done_transition):
        old_transitions = self._get_transition_images([done_transition.destination_state.pk])

        iteration = done_transition.iteration + 1
        regenerated_transitions = set()
        while old_transitions:
            for old_transition in old_transitions:
                cycled_transition = Transition.objects.create(
                    source_state=old_transition.source_state,
                    destination_state=old_transition.destination_state,
                    workflow=old_transition.workflow,
                    object_id=old_transition.workflow_object.pk,
                    content_type=old_transition.content_type,
                    status=Transition.PENDING,
                    iteration=iteration,
                    meta=old_transition.meta
                )

                for old_approval in old_transition.transition_approvals.all():
                    cycled_approval = TransitionApproval.objects.create(
                        transition=cycled_transition,
                        workflow=old_approval.workflow,
                        object_id=old_approval.workflow_object.pk,
                        content_type=old_approval.content_type,
                        priority=old_approval.priority,
                        status=TransitionApproval.PENDING,
                        meta=old_approval.meta
                    )
                    cycled_approval.permissions.set(old_approval.permissions.all())
                    cycled_approval.groups.set(old_approval.groups.all())

            regenerated_transitions.add((old_transition.source_state, old_transition.destination_state))

            old_transitions = self._get_transition_images(old_transitions.values_list("destination_state__pk", flat=True)).exclude(
                six.moves.reduce(lambda agg, q: q | agg, [Q(source_state=source_state, destination_state=destination_state)
                                                          for source_state, destination_state in regenerated_transitions], Q(pk=-1))
            )

            iteration += 1

    def get_state(self):
        workflow_object = self.workflow_object
        return getattr(workflow_object, self.status_field)

    def set_state(self, state_value, commit=True):
        workflow_object = self.workflow_object
        setattr(workflow_object, self.status_field, state_value)
        if commit:
            workflow_object.save(update_fields=[self.status_field])
