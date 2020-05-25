from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


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
