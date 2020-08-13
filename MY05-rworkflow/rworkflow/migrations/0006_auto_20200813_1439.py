# Generated by Django 2.2.15 on 2020-08-13 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0005_remove_workflow_order_relation_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='state',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='transitionapproval',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='transitionapproval',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='transitionapprovalmeta',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='transitionapprovalmeta',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='transitionmeta',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='transitionmeta',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='wforder',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='wforder',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='workflow',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='workflow',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='workflowcategory',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='workflowcategory',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='created_by',
            field=models.CharField(blank=True, db_index=True, default='', max_length=80, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='updated_by',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='修改者'),
        ),
        migrations.AlterField(
            model_name='wforder',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='申请者'),
        ),
    ]
