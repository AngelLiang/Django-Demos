from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets import views2
from snippets import views3
from snippets import views4
from snippets import views5


urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    # path('snippets/', views2.snippet_list),
    # path('snippets/<int:pk>', views2.snippet_detail),

    # path('snippets/', views3.SnippetList.as_view()),
    # path('snippets/<int:pk>/', views3.SnippetDetail.as_view()),

    path('snippets/', views5.SnippetList.as_view()),
    path('snippets/<int:pk>/', views5.SnippetDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
