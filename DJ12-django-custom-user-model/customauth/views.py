from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)

from customauth.serializer import UserSerializer

from utils import JsonResponse
from utils import status_code


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user, context={'request': request})
    # return Response(serializer.data)
    return JsonResponse(data=serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_token_view(request, format=None):
    """
    HTTP header:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    """

    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)


class AuthTokenApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data or request.json
        serializer = self.serializer_class(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, is_created = Token.objects.get_or_create(user=user)
        return Response({
            'code': status_code.CODE_SUCCESS,
            'is_created': is_created,
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_token(request, format=None):
    """
    HTTP header:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    """
    user = request.user
    token = request.auth
    return Response({
        'code': status_code.CODE_SUCCESS,
        'message': '成功登出',
    })
