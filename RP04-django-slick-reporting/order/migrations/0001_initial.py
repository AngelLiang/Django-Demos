# Generated by Django 3.0.8 on 2020-07-07 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='姓名')),
                ('phone', models.CharField(max_length=255, verbose_name='联系电话')),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='订单日期')),
                ('title', models.CharField(default='', max_length=255, verbose_name='标题')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=11, verbose_name='总金额')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Customer', verbose_name='客户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='单价')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='单价')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=11, verbose_name='总价')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='订单')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Product', verbose_name='产品')),
            ],
            options={
                'verbose_name': '订单明细',
                'verbose_name_plural': '订单明细',
            },
        ),
    ]
