# from rest_framework import viewsets
from rest_framework import permissions

from customauth.models import Organization
from customauth.serializer import OrganizationSerializer
from .base import BaseViewSet


class OrganizationViewSet(BaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
