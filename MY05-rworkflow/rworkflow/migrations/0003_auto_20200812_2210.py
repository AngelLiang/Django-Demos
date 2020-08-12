# Generated by Django 2.2.15 on 2020-08-12 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rworkflow', '0002_auto_20200812_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transitionapprovalmeta',
            old_name='next_user_handler',
            new_name='user_handler_function',
        ),
        migrations.RenameField(
            model_name='transitionapprovalmeta',
            old_name='handler',
            new_name='user_handler_sql',
        ),
        migrations.AlterUniqueTogether(
            name='transitionapprovalmeta',
            unique_together={('workflow', 'transition_meta', 'priority')},
        ),
    ]
