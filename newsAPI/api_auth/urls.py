from django.urls import path, include

from .views import CreateUserView, ObtainTokensPairView, ObtainAccessTokenView


app_name = 'api_auth'

urlpatterns = [
    path('signup/', CreateUserView.as_view({'post': 'create'}), name='signup'),
    path('users/', CreateUserView.as_view({'get': 'list'}), name='user_list'),
    path('user/<int:pk>/', CreateUserView.as_view({'get': 'retrieve'}), name='user'),
    path('user/<int:pk>/ban/', CreateUserView.as_view({'post': 'ban_user'}), name='user'),
    path('user/<int:pk>/unban/', CreateUserView.as_view({'post': 'unban_user'}), name='user'),
    path('token/', ObtainTokensPairView.as_view(), name='token'),
    path('token/update/', ObtainAccessTokenView.as_view(), name='access_token'),
]