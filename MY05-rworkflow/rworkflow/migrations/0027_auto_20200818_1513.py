# Generated by Django 2.2.15 on 2020-08-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0026_transitionapprovalmeta_rule_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='transitionapprovalmeta',
            name='rule_memo',
            field=models.TextField(blank=True, default='', verbose_name='条件判断规则说明'),
        ),
        migrations.AlterField(
            model_name='transitionapprovalmeta',
            name='rule_enabled',
            field=models.BooleanField(default=False, verbose_name='是否启用条件判断规则？'),
        ),
    ]
