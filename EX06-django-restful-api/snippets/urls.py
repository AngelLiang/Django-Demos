from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets import views2
from snippets import views3
from snippets import views4
from snippets import views5
from snippets import views6


urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    # path('snippets/', views2.snippet_list),
    # path('snippets/<int:pk>', views2.snippet_detail),

    # path('snippets/', views3.SnippetList.as_view()),
    # path('snippets/<int:pk>/', views3.SnippetDetail.as_view()),

    # path('snippets/', views5.SnippetList.as_view()),
    # path('snippets/<int:pk>/', views5.SnippetDetail.as_view()),

]
# urlpatterns = format_suffix_patterns(urlpatterns)


# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly

# urlpatterns += format_suffix_patterns([
#     # path('', api_root),
#     path('snippets/', views6.snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', views6.snippet_detail, name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/',
#          views6.snippet_highlight, name='snippet-highlight'),
#     # path('users/', views6.user_list, name='user-list'),
#     # path('users/<int:pk>/', views6.user_detail, name='user-detail')
# ])


# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers

from rest_framework.routers import DefaultRouter
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views6.SnippetViewSet)
# router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns += [
    path('', include(router.urls)),
]
