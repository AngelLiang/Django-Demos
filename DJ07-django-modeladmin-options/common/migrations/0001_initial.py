# Generated by Django 3.0.3 on 2020-03-02 05:38

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='标签名')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('slug', models.SlugField(default='')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('is_delete', models.BooleanField(default=False, verbose_name='已删除')),
                ('create_date', models.DateField(auto_now=True, verbose_name='创建日期')),
                ('create_time', models.TimeField(auto_now=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('view_count', models.IntegerField(default=0, verbose_name='浏览次数')),
                ('money', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=8)),
                ('price', models.FloatField(blank=True, default=0.0)),
                ('tags', models.ManyToManyField(to='common.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-update_datetime'],
            },
        ),
    ]
