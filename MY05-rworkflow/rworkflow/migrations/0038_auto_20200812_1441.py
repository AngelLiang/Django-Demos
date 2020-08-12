# Generated by Django 2.2.15 on 2020-08-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0037_auto_20200812_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='transitionapproval',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='transitionapprovalmeta',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='transitionapprovalmeta',
            name='email_notice',
            field=models.BooleanField(default=False, verbose_name='邮件通知'),
        ),
        migrations.AlterField(
            model_name='transitionmeta',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='workflowcategory',
            name='code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='workflowcategory',
            name='pinyin',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='拼音/英文'),
        ),
        migrations.AlterField(
            model_name='workflowcategory',
            name='short',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='简称'),
        ),
    ]
