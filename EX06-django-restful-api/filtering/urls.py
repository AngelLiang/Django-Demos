from django.urls import path, include
from django.conf.urls import url

from .apis import (
    CurrentUserPurchaseList,
    PurchaseListByUsername,
    PurchaseListSearch,
    PurchaseListOrder,
)


urlpatterns = [
    path('current_user/pruchases/', CurrentUserPurchaseList.as_view()),
    path('purchases/search/', PurchaseListSearch.as_view()),
    path('purchases/order/', PurchaseListOrder.as_view()),
    url(r'^purchases/(?P<username>.+)/$', PurchaseListByUsername.as_view()),
]
