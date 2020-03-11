from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis import AlbumViewSet, TrackViewSet


router = DefaultRouter()
router.register(r'album', AlbumViewSet)
router.register(r'track', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
