from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomAuthToken(ObtainAuthToken):
    """
    HTTP header:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    """

    # def get(self, request, *args, **kwargs):
    #     content = {
    #         # `django.contrib.auth.User` instance.
    #         'user': str(request.user),
    #         'auth': str(request.auth),  # None
    #     }
    #     return Response(content)

    parser_classes = (FormParser, MultiPartParser)

    # 自定义swagger
    @swagger_auto_schema(
        operation_summary='用户登录，获取帐号的token',
        operation_description='',
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         'username': openapi.Schema(
        #             in_=openapi.IN_BODY,
        #             type=openapi.TYPE_STRING,
        #             description='用户名'
        #         ),
        #         'password': openapi.Schema(
        #             in_=openapi.IN_BODY,
        #             type=openapi.TYPE_STRING,
        #             description='密码'
        #         ),
        #     }
        # )

        # 表单
        manual_parameters=[
            openapi.Parameter(
                name='username',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description='用户名',
            ),
            openapi.Parameter(
                name='password',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description='密码',
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
