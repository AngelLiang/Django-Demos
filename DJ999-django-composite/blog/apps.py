from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig
    """
    name = 'blog'
    label = '博客'
    verbose_name = '博客'
