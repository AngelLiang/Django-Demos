from django.urls import path
from django.conf.urls import url, include

from .apis import router
from .views import (
    AuthTokenApi, get_token_view, get_user_info,
    delete_token
)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('login', AuthTokenApi.as_view()),
    path('logout', delete_token),
    path('user/info', get_user_info),
    path('token', AuthTokenApi.as_view()),
    path('token/detail', get_token_view),
]
