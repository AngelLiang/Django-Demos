# Generated by Django 3.0.7 on 2020-06-23 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('D', 'draft'), ('P', 'published')], default='D', max_length=1),
        ),
    ]
