# Generated by Django 2.2.15 on 2020-08-13 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0004_auto_20200813_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='order_relation_config',
        ),
    ]
