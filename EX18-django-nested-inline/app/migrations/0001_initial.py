# Generated by Django 2.2.20 on 2021-04-25 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LevelOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TopLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LevelTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.LevelOne')),
            ],
        ),
        migrations.CreateModel(
            name='LevelThree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.LevelTwo')),
            ],
        ),
        migrations.AddField(
            model_name='levelone',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TopLevel'),
        ),
    ]
