import random

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from django_seed import Seed
from faker import Faker

seeder = Seed.seeder(locale='zh_CN')
faker = Faker('zh_CN')


class Command(BaseCommand):
    help = '生成虚拟订单'

    @transaction.atomic()
    def handle(self, *args, **options):
        from order.models import Order, OrderItem

        seeder.add_entity(Order, 10, {})

        inserted_pks = seeder.execute()

        # print(inserted_pks)
        for oid in inserted_pks[Order]:
            order = Order.objects.get(id=oid)
            for _ in range(3):
                OrderItem.objects.create(
                    order=order,
                    price=random.randrange(10, 100),
                    quantity=random.randrange(1, 10),
                )
