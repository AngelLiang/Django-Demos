# Generated by Django 2.2.14 on 2020-07-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0009_auto_20200729_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='wforder',
            name='description',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='描述'),
        ),
    ]
