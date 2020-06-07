from django.contrib.auth.models import Group
# from rest_framework import serializers

from .base import BaseSerializer


class GroupSerializer(BaseSerializer):
    class Meta:
        model = Group
        fields = [
            'name',
            'url',
        ]
