from django.contrib import admin

# Register your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mqtt.publisher.models import Data as MQTTData


@receiver(post_save, sender=MQTTData)
def auto_update(sender, instance, **kwargs):
    """添加或更新 Data 的时候会发布消息"""
    print(f'publish to {instance.topic.name}')
    instance.update_remote()
