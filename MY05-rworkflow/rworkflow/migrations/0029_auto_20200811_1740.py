# Generated by Django 2.2.15 on 2020-08-11 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0028_auto_20200811_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transitionmeta',
            name='destination_state_value',
        ),
        migrations.RemoveField(
            model_name='transitionmeta',
            name='source_state_value',
        ),
    ]
