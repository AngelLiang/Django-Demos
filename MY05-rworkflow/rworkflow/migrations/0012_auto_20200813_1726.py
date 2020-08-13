# Generated by Django 2.2.15 on 2020-08-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0011_auto_20200813_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='status',
            field=models.CharField(choices=[('pending', '准备中'), ('cancelled', '已取消'), ('done', '已完成'), ('jumped', '已跳转')], db_index=True, default='pending', max_length=16, verbose_name='状态'),
        ),
    ]
