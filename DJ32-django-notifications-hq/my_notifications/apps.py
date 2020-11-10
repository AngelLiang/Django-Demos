from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MyNotificationsConfig(AppConfig):
    name = 'my_notifications'
    verbose_name = _('我的通知')
