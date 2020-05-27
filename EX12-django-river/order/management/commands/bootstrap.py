from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from river.models import State, Workflow, TransitionApprovalMeta, TransitionMeta

from order.models import Order, OrderItem, Product


# noinspection DuplicatedCode
class Command(BaseCommand):
    help = 'Bootstrapping database with necessary items'

    @transaction.atomic()
    def handle(self, *args, **options):
        workflow_content_type = ContentType.objects.get_for_model(Workflow)
        order_content_type = ContentType.objects.get_for_model(Order)
        order_item_content_type = ContentType.objects.get_for_model(OrderItem)

        # 获取权限
        add_order_permission = Permission.objects.get(codename="add_order", content_type=order_content_type)
        change_order_permission = Permission.objects.get(codename="change_order", content_type=order_content_type)
        delete_order_permission = Permission.objects.get(codename="delete_order", content_type=order_content_type)

        add_orderitem_permission = Permission.objects.get(
            codename="add_orderitem", content_type=order_item_content_type)
        change_orderitem_permission = Permission.objects.get(
            codename="change_orderitem", content_type=order_item_content_type)
        delete_orderitem_permission = Permission.objects.get(
            codename="delete_orderitem", content_type=order_item_content_type)

        view_workflow_permission = Permission.objects.get(codename="view_workflow", content_type=workflow_content_type)

        # 采购组长
        team_leader_group, _ = Group.objects.update_or_create(name="采购组长")
        team_leader_group.permissions.set([add_order_permission, change_order_permission, delete_order_permission,
                                           add_orderitem_permission, change_orderitem_permission, delete_orderitem_permission,
                                           view_workflow_permission])
        # 采购员
        purchaser_group, _ = Group.objects.update_or_create(name="采购员")
        purchaser_group.permissions.set([add_order_permission, change_order_permission,
                                         add_orderitem_permission, change_orderitem_permission, delete_order_permission,
                                         view_workflow_permission])

        # 创建状态
        draft_state, _ = State.objects.get_or_create(label="草稿", slug="draft")
        issued_state, _ = State.objects.get_or_create(label="已发货", slug="issued")
        partreceived_state, _ = State.objects.get_or_create(label="部分收货", slug="partreceived")
        received_state, _ = State.objects.get_or_create(label="收货完成", slug="received")
        closed_state, _ = State.objects.get_or_create(label="关闭", slug="closed")

        # 更新或创建工作流，并设置初始化状态
        workflow, _ = Workflow.objects.update_or_create(
            content_type=order_content_type, field_name="status", defaults={"initial_state": draft_state})

        # 草稿 -> 已发货
        draft_to_issued, _ = TransitionMeta.objects.get_or_create(
            workflow=workflow, source_state=draft_state, destination_state=issued_state)
        # 已发货 -> 部分收货
        issued_to_partreceived, _ = TransitionMeta.objects.get_or_create(
            workflow=workflow, source_state=issued_state, destination_state=partreceived_state)
        # 已发货 -> 收货完成
        issued_to_received, _ = TransitionMeta.objects.get_or_create(
            workflow=workflow, source_state=issued_state, destination_state=received_state)
        # 部分收货 -> 收货完成
        partreceived_to_received, _ = TransitionMeta.objects.get_or_create(
            workflow=workflow, source_state=partreceived_state, destination_state=received_state)
        # 收货完成 -> 已发货
        # received_to_issued, _ = TransitionMeta.objects.get_or_create(
        #     workflow=workflow, source_state=received_state, destination_state=issued_state)
        # 收货完成 -> 关闭
        # received_to_closed, _ = TransitionMeta.objects.get_or_create(
        #     workflow=workflow, source_state=received_state, destination_state=closed_state)

        # 草稿 -> 已发货
        draft_to_issued_meta, _ = TransitionApprovalMeta.objects.get_or_create(
            workflow=workflow, transition_meta=draft_to_issued)
        draft_to_issued_meta.groups.set([purchaser_group])

        # 已发货 -> 部分收货
        issued_to_partreceived_meta, _ = TransitionApprovalMeta.objects.get_or_create(
            workflow=workflow, transition_meta=issued_to_partreceived)
        issued_to_partreceived_meta.groups.set([purchaser_group])

        # 部分收货 -> 收货完成
        partreceived_to_received_meta, _ = TransitionApprovalMeta.objects.get_or_create(
            workflow=workflow, transition_meta=partreceived_to_received)
        partreceived_to_received_meta.groups.set([purchaser_group])

        # 已发货 -> 收货完成
        issued_to_received_meta, _ = TransitionApprovalMeta.objects.get_or_create(
            workflow=workflow, transition_meta=issued_to_received)
        issued_to_received_meta.groups.set([purchaser_group])

        # 收货完成 -> 已发货
        # received_to_issued_meta, _ = TransitionApprovalMeta.objects.get_or_create(
        #     workflow=workflow, transition_meta=received_to_issued)
        # received_to_issued_meta.groups.set([team_leader_group])

        # 收货完成 -> 关闭
        # received_to_closed_meta, _ = TransitionApprovalMeta.objects.get_or_create(
        #     workflow=workflow, transition_meta=received_to_closed)
        # received_to_closed_meta.groups.set([team_leader_group])

        # 超管
        root = User.objects.filter(username="root").first() or User.objects.create_superuser("root", "", "q1w2e3r4")
        root.groups.set([team_leader_group, purchaser_group])

        # 采购组长
        team_leader_1 = User.objects.filter(username="team_leader_1").first(
        ) or User.objects.create_user("team_leader_1", password="q1w2e3r4", is_staff=True)
        team_leader_1.groups.set([team_leader_group])

        # 采购员
        purchaser_1 = User.objects.filter(username="purchaser_1").first(
        ) or User.objects.create_user("purchaser_1", password="q1w2e3r4", is_staff=True)
        purchaser_1.groups.set([purchaser_group])

        Product.objects.get_or_create(name='测试产品')

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
