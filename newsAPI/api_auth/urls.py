from django.urls import path, include

from .views import CreateUserView, ObtainTokensPairView


app_name = 'api_auth'

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('token/', ObtainTokensPairView.as_view(), name='token'),
]