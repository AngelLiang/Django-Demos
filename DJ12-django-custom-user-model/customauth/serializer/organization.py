from rest_framework import serializers

from customauth.models import Organization
from .base import BaseSerializer


class OrganizationSerializer(BaseSerializer):

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'code',
            'leader',
            'parent_id',
            'created_at',
            'updated_at',
            'url',
        ]
