from django.conf.urls import url

from .views import approve_order

urlpatterns = [
    url(r'^approve_order/(?P<order_id>\d+)/(?P<next_state_id>\d+)/$',
        approve_order, name='approve_order'),
]
