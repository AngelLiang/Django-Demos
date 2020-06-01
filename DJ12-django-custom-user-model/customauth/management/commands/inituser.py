from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from customauth.models import User, Role, Organization


class Command(BaseCommand):
    help = '初始化虚拟用户数据'

    @transaction.atomic()
    def handle(self, *args, **options):
        superuser = User.objects.filter(username="admin").first(
        ) or User.objects.create_superuser(
            "admin", password="admin"
        )

        root_org, _ = Organization.objects.update_or_create(
            name="XX集团", created_by=superuser, updated_by=superuser)
        org, _ = Organization.objects.update_or_create(
            name="总部", parent=root_org, created_by=superuser, updated_by=superuser)
        org1, _ = Organization.objects.update_or_create(
            name="分部1", parent=root_org, created_by=superuser, updated_by=superuser)
        org1, _ = Organization.objects.update_or_create(
            name="分部2", parent=root_org, created_by=superuser, updated_by=superuser)

        dev_org, _ = Organization.objects.update_or_create(
            name="开发部门", parent=org, created_by=superuser, updated_by=superuser)
        test_org, _ = Organization.objects.update_or_create(
            name="测试部门", parent=org, created_by=superuser, updated_by=superuser)
        oper_org, _ = Organization.objects.update_or_create(
            name="运营部门", parent=org, created_by=superuser, updated_by=superuser)

        dev_org1, _ = Organization.objects.update_or_create(
            name="开发部门", parent=org1, created_by=superuser, updated_by=superuser)
        test_org1, _ = Organization.objects.update_or_create(
            name="测试部门", parent=org1, created_by=superuser, updated_by=superuser)
        oper_org1, _ = Organization.objects.update_or_create(
            name="运营部门", parent=org1, created_by=superuser, updated_by=superuser)

        admin, _ = Role.objects.update_or_create(name="管理员", created_by=superuser, updated_by=superuser)
        chairman, _ = Role.objects.update_or_create(name="董事长", created_by=superuser, updated_by=superuser)
        manager, _ = Role.objects.update_or_create(name="经理", created_by=superuser, updated_by=superuser)
        leader, _ = Role.objects.update_or_create(name="组长", created_by=superuser, updated_by=superuser)
        member, _ = Role.objects.update_or_create(name="组员", created_by=superuser, updated_by=superuser)

        chairman_user = User.objects.filter(username="chairman").first(
        ) or User.objects.create_user(
            "chairman", password="chairman", is_staff=True,
            organization=root_org,
        )
        chairman_user.roles.set([chairman])

        manager_user = User.objects.filter(username="manager").first(
        ) or User.objects.create_user(
            "manager", password="manager", is_staff=True,
            organization=dev_org,
        )
        manager_user.roles.set([manager])

        dev_leader = User.objects.filter(username="leader1").first(
        ) or User.objects.create_user(
            "leader1", password="leader1", is_staff=True,
            organization=dev_org,
        )
        dev_leader.roles.set([leader])

        dev_member1 = User.objects.filter(username="dev_member1").first(
        ) or User.objects.create_user(
            "dev_member1", password="dev_member1", is_staff=True,
            organization=dev_org,
        )
        dev_member1.roles.set([member])

        dev_member2 = User.objects.filter(username="dev_member2").first(
        ) or User.objects.create_user(
            "dev_member2", password="dev_member2", is_staff=True,
            organization=dev_org,
        )
        dev_member2.roles.set([member])

        dev_member3 = User.objects.filter(username="dev_member3").first(
        ) or User.objects.create_user(
            "dev_member3", password="dev_member3", is_staff=True,
            organization=dev_org,
        )
        dev_member3.roles.set([member])
