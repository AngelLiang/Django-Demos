# Generated by Django 3.0.5 on 2020-04-13 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_author_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
    ]
