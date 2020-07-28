from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthlogConfig(AppConfig):
    name = 'authlog'
    verbose_name = _('登录日志')
