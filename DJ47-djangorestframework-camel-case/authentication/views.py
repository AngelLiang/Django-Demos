from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    authentication_classes = [
        SessionAuthentication,
        # https://www.django-rest-framework.org/api-guide/authentication/#basicauthentication
        BasicAuthentication,
        # https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
        TokenAuthentication
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            # `django.contrib.auth.User` instance.
            'user': str(request.user),
            'auth': str(request.auth),  # None
            'djangorestframework_camel_case': 'test',
            'Djangorestframework_camel_case2': 'test'
        }
        return Response(content)
