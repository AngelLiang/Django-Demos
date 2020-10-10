from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken import views

from .views import ExampleView
from .auth_token import CustomAuthToken


urlpatterns = [
    path('user/info/', ExampleView.as_view()),
]
urlpatterns += [
    # url(r'^api-token-auth/', views.obtain_auth_token)
    path('token/', CustomAuthToken.as_view())
]
