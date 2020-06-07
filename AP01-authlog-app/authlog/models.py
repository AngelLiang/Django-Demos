from django.db import models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


class AuthEntry(models.Model):
    USER_LOGGED_IN = 'user_logged_in'
    USER_LOGGED_OUT = 'user_logged_out'
    USER_LOGGED_FAILED = 'user_login_failed'
    ACTION_CHOICES = [
        (USER_LOGGED_IN, '用户登录成功'),
        (USER_LOGGED_OUT, '用户登出成功'),
        (USER_LOGGED_FAILED, '用户登录失败'),
    ]

    action = models.CharField('动作', max_length=64, choices=ACTION_CHOICES)
    action_at = models.DateTimeField('动作时间', auto_now_add=True)
    ip = models.GenericIPAddressField('IP', null=True)
    username = models.CharField('用户名', max_length=255, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='用户',
        related_name='+',
    )

    def __str__(self):
        return f'{self.username}在{self.action_at}进行{self.action}操作'

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuthEntry.objects.create(action=AuthEntry.USER_LOGGED_IN,
                             ip=ip, username=user.username, user=user)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuthEntry.objects.create(action=AuthEntry.USER_LOGGED_OUT,
                             ip=ip, username=user.username, user=user)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    # print(credentials)
    ip = request.META.get('REMOTE_ADDR')
    AuthEntry.objects.create(
        action=AuthEntry.USER_LOGGED_FAILED,
        ip=ip,
        username=credentials.get('username', None)
    )
