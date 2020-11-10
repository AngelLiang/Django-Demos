from django.db import models
from django.utils.translation import ugettext_lazy as _

from notifications.models import Notification


class MyNotification(Notification):
    class Meta:
        managed = False
        proxy = True
        verbose_name = _('我的通知')
        verbose_name_plural = _('我的通知')
