from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
from river.models import State

from .models import Order


def approve_order(request, order_id, next_state_id=None):
    order = get_object_or_404(Order, pk=order_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        order.river.status.approve(
            as_user=request.user, next_state=next_state)
        # admin:<app>_<model>_changelist
        return redirect(reverse('admin:order_order_changelist'))
    except Exception as e:
        return HttpResponse(e.message)
