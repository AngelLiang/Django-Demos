
from django.contrib import admin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from admin_totals.admin import ModelAdminTotals

from . import models


@admin.register(models.Expense)
class ExpenseModelAdmin(ModelAdminTotals):
    list_display = ['amount', 'has_invoice', 'total']
    list_totals = [('amount', lambda field: Coalesce(Sum(field), 0)), ('total', Avg)]
