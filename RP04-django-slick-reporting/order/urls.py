from django.contrib import admin
from django.urls import path

from .views import OrderItemReportView

urlpatterns = [
    path('order-item-report-view/', OrderItemReportView.as_view()),
]
