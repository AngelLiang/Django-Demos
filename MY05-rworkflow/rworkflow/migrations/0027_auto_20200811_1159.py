# Generated by Django 2.2.15 on 2020-08-11 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0026_auto_20200811_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='can_edit',
            field=models.BooleanField(default=False, verbose_name='可编辑？'),
        ),
        migrations.AddField(
            model_name='state',
            name='can_take',
            field=models.BooleanField(default=False, verbose_name='可接单？'),
        ),
    ]
