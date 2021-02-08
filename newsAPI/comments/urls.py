from django.urls import path

from .views import CommentViewSet

app_name = 'comments'

urlpatterns = [
    path('', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'post': 'answer'})),
]