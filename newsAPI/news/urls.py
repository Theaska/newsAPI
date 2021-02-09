from django.urls import path
from .views import NewsPostListCreate, NewsPostListGetDeleteUpdate


app_name = 'news'

urlpatterns = [
    path('', NewsPostListCreate.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', NewsPostListGetDeleteUpdate.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'partial_update'})),
]