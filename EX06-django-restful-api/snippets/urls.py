from rest_framework.routers import DefaultRouter
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

# Create a router and register our viewsets with it.
router = DefaultRouter()

# basename - the base to use for the URL names that are created.
# action - the name of the current action (e.g., list, create).
# detail - boolean indicating if the current action is configured for a list or detail view.
# suffix - the display suffix for the viewset type - mirrors the detail attribute.
# name - the display name for the viewset. This argument is mutually exclusive to suffix.
# description - the display description for the individual view of a viewset.
router.register(r'snippets', views6.SnippetViewSet, basename='snippets')
# router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns += router.urls
