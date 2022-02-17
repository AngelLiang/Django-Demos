from django.contrib import admin

from django.contrib import admin
from djtoolbox.admin.fieldsets import FieldsetsMixin

from ..models import DictionarytItem
from django.utils.translation import gettext_lazy as _
from djtoolbox.django_admin_inline_paginator.admin import TabularInlinePaginated


class DictionarytItemInline(FieldsetsMixin, TabularInlinePaginated, admin.TabularInline):
    model = DictionarytItem
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('code', 'label',)
        }),
    )
