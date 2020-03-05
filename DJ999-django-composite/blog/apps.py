from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig
    """

    # https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.name
    name = 'blog'

    # https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.label
    # label = 'blog'

    # https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.verbose_name
    verbose_name = '博客'
