from django.contrib import admin

# Register your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mqtt.publisher.models import Data as MQTTData
from django_mqtt.publisher.models import Client
from django_mqtt.publisher.signals import mqtt_publish


def then_publish(sender, client, userdata, mid, **kwargs):
    if not isinstance(client, Client):
        raise AttributeError('client must be Client object')
    print(mid)


mqtt_publish.connect(receiver=then_publish, sender=Client,
                     dispatch_uid='my_django_mqtt_then_publish')


@receiver(post_save, sender=MQTTData)
def auto_update(sender, instance, **kwargs):
    """添加或更新 Data 的时候会发布消息"""
    print(kwargs)
    print(f'publish to {instance.topic.name}')
    instance.update_remote()
