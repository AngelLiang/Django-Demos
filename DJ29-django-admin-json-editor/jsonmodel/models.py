from django.db import models
from django.contrib.postgres.fields import JSONField


def defaultjsondata():
    return {
        'text': 'some text',
        'status': False,
        'html': '<h1>Default</h1>',
    }


class JSONModel(models.Model):
    data = JSONField(default=defaultjsondata)


class ArrayJSONModel(models.Model):
    roles = JSONField(default=list)


class Tag(models.Model):
    name = models.CharField('name', max_length=10)
