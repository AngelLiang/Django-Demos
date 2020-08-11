from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .base import BaseAdmin


class WorkflowCategoryAdmin(BaseAdmin):
    list_display = (
        'code', 'name', 'spec', 'is_active'
    )
    list_display_links = ('code', 'name',)

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'spec',
            ),
        }),
        (_('信息'), {
            'fields': (
                'code',
                'is_active',
                'weight',
            ),
        }),
    )
