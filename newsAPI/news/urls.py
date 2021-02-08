from django.urls import path
from .views import NewsPostViewSet


app_name = 'news'

urlpatterns = [
    path('', NewsPostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', NewsPostViewSet.as_view({'get': 'retrieve'})),
]