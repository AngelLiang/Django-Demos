from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField('分类名称', max_length=128)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField('设备', max_length=128)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='分类'
    )

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField('属性', max_length=64)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE,
        verbose_name='设备'
    )

    def __str__(self):
        return self.name


class Value(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE,
        verbose_name='属性'
    )
    value = models.CharField('属性值', max_length=255)

    def __str__(self):
        return f'{self.attribute} - {self.value}'
