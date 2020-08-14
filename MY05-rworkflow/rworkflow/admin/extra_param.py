
from .base import BaseAdmin
from django.utils.translation import ugettext_lazy as _


class ExtraParamMetaAdmin(BaseAdmin):

    list_display = (
        'code', 'name', 'value_tp',
        'memo', 'is_active', 'weight',
    )
    fieldsets = (
        (None, {
            'fields': (
                'code',
                'name',
                'value_tp',
                ('is_choice_combo', 'is_choice_async',),
                'memo',
                'is_active',
                'weight',
            ),
        }),
        # (_('信息'), {
        #     'fields': (
        #         'created_at',
        #         'updated_at',
        #         'created_by',
        #         'updated_by',
        #     ),
        # }),
    )
    readonly_fields = (
        'created_at', 'updated_at',
        'created_by', 'updated_by'
    )


class ExtraParamAdmin(BaseAdmin):

    list_display = (
        'name', 'value_tp',
        'memo', 'weight',
    )
