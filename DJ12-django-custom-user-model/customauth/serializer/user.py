from rest_framework import serializers
from django.contrib.auth import get_user_model

# from customauth.models import User
from .base import BaseSerializer

User = get_user_model()


class UserSerializer(BaseSerializer):
    # username = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username', 'email',
            'name',
            # 'is_staff',
            'is_active',
            'date_joined', 'last_login',
            'url',
        ]


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
