from rest_framework import routers

from .user import UserViewSet
from .role import RoleViewSet
from .organization import OrganizationViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'organizations', OrganizationViewSet)
