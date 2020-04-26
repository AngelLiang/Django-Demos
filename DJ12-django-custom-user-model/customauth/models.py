from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    name = models.CharField('组织名称', max_length=80)

    def __str__(self):
        return self.name


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='所属组织',
    )
