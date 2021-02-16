from django.urls import path

from .views import UserViewSet, ObtainTokensPairView, ObtainAccessTokenView


app_name = 'api_auth'

urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'create'}), name='signup'),
    
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user_list'),
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user'),
    path('user/<int:pk>/ban/', UserViewSet.as_view({'post': 'ban_user'}), name='user_ban'),
    path('user/<int:pk>/unban/', UserViewSet.as_view({'post': 'unban_user'}), name='user_unban'),

    path('token/', ObtainTokensPairView.as_view(), name='get_token'),
    path('token/update/', ObtainAccessTokenView.as_view(), name='update_token'),
]