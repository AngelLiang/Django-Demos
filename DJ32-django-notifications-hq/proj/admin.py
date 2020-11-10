from django.contrib import admin
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from notifications.signals import notify


class MyAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['notifications'] = request.user.notifications.all()
        return super().index(request, extra_context)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    notify.send(user, recipient=user, verb='登录', description=ip)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    notify.send(user, recipient=user, verb='登出', description=ip)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    username = credentials.get('username', None)
