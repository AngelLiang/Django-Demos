"""
ModelViewSet: https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset

The ModelViewSet class inherits from GenericAPIView and includes implementations for 
various actions, by mixing in the behavior of the various mixin classes.
"""
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import routers
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, PasswordSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[])
    def set_password(self, request, pk=None):
        """设置密码"""
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
