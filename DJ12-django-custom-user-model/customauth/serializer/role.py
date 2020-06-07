
from rest_framework import serializers

from customauth.models import Role
from .base import BaseSerializer


class RoleSerializer(BaseSerializer):

    class Meta:
        model = Role
        fields = [
            'id',
            'name', 'code',
            'created_at',
            'updated_at',
            'url',
        ]
