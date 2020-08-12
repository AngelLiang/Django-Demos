# Generated by Django 2.2.15 on 2020-08-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0036_auto_20200812_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transitionapproval',
            name='can_take',
        ),
        migrations.RemoveField(
            model_name='transitionapprovalmeta',
            name='can_take',
        ),
        migrations.AddField(
            model_name='transitionapproval',
            name='can_suggestion',
            field=models.BooleanField(default=False, verbose_name='处理人可填写处理意见？'),
        ),
        migrations.AddField(
            model_name='transitionapproval',
            name='need_take',
            field=models.BooleanField(default=False, verbose_name='需要处理人接单？'),
        ),
        migrations.AddField(
            model_name='transitionapprovalmeta',
            name='need_take',
            field=models.BooleanField(default=False, verbose_name='需要处理人接单？'),
        ),
        migrations.AlterField(
            model_name='transitionapproval',
            name='can_edit',
            field=models.BooleanField(default=False, verbose_name='处理人可编辑？'),
        ),
        migrations.AlterField(
            model_name='transitionapprovalmeta',
            name='can_edit',
            field=models.BooleanField(default=False, verbose_name='处理人可编辑？'),
        ),
        migrations.AlterField(
            model_name='transitionapprovalmeta',
            name='can_suggestion',
            field=models.BooleanField(default=False, verbose_name='处理人可填写处理意见？'),
        ),
    ]
