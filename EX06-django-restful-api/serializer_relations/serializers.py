import time

from rest_framework import serializers

from .models import Album, Track


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        # fields = ['title', 'duration', 'order']
        fields = '__all__'


class TrackListingField(serializers.RelatedField):
    """
    https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    """

    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(value.duration))
        return 'Track %d: %s (%s)' % (value.order, value.name, duration)


class AlbumSerializer(serializers.ModelSerializer):
    # StringRelatedField
    # https://www.django-rest-framework.org/api-guide/relations/#stringrelatedfield
    # tracks = serializers.StringRelatedField(many=True)

    # PrimaryKeyRelatedField
    # https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
    # tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # HyperlinkedRelatedField
    # https://www.django-rest-framework.org/api-guide/relations/#hyperlinkedrelatedfield
    # tracks = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='track-detail'
    # )

    # SlugRelatedField
    # https://www.django-rest-framework.org/api-guide/relations/#slugrelatedfield
    # tracks = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='title'
    # )

    # HyperlinkedIdentityField
    # https://www.django-rest-framework.org/api-guide/relations/#hyperlinkedidentityfield
    # track_listing = serializers.HyperlinkedIdentityField(
    #     view_name='track-list')

    # Nested relationships
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    tracks = TrackSerializer(many=True, read_only=True)

    # https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    # tracks = TrackListingField(many=True)

    class Meta:
        model = Album
        fields = [
            'album_name', 'artist', 'tracks',
            # 'track_listing'
        ]

    def create(self, validated_data):
        """
        https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
        """
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
