from rest_framework import permissions

from customauth.models import Group
from customauth.serializer import GroupSerializer
from .base import BaseViewSet


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
