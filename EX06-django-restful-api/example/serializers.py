from django.contrib.auth.models import User, Group
from rest_framework import serializers

from snippets.models import Snippet


class UserSerializer(serializers.HyperlinkedModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'snippets']

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['password']
