from rest_framework import permissions

from customauth.models import Role
from customauth.serializer import RoleSerializer
from .base import BaseViewSet


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
