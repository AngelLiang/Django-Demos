from django.db import models


class TempUser(models.Model):
    username = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)

    class Meta:
        # managed 设置为 False 以免 Django 迁移该模型
        # https://docs.djangoproject.com/en/3.0/ref/models/options/#django.db.models.Options.managed
        managed = False
        db_table = "temp_user"
