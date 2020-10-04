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
        from order.models import Customer, Product

        cc = Customer.objects.count()
        if cc == 0:
            seeder.add_entity(Customer, 3, {
                'name': lambda x: faker.name(),
                'phone': lambda x: faker.phone_number(),
            })
            seeder.execute()

        pc = Product.objects.count()
        if pc == 0:
            seeder.add_entity(Product, 5, {
                'name': lambda x: faker.word(),
                'price': lambda x: random.randrange(10, 100),
            })
            seeder.execute()

        seeder.add_entity(Order, 10, {
            'title': lambda x: faker.sentence(),
            'description': lambda x: faker.text(),
            'customer': lambda x: Customer.objects.get(id=random.randrange(1, Customer.objects.count()))
        })

        inserted_pks = seeder.execute()

        # print(inserted_pks)
        for oid in inserted_pks[Order]:
            order = Order.objects.get(id=oid)

            for _ in range(3):
                OrderItem.objects.create(
                    order=order,
                    price=random.randrange(10, 100),
                    quantity=random.randrange(1, 10),
                    product=Product.objects.get(id=random.randrange(1, Product.objects.count()))
                )
