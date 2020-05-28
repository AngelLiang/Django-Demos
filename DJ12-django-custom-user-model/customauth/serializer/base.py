from rest_framework import serializers


# class BaseSerializer(serializers.HyperlinkedModelSerializer):
#     pass


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
