from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import permissions

from .serializers import UserSerializer, ObtainTokensPairSerializer, ObtainAccessTokenSerializer


class CreateUserView(ModelViewSet):
    model = get_user_model()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def get_permissions(self):
        permissions_lst = []
        if self.action in ('list', 'ban_user'):
            permissions_lst.append(permissions.IsAdminUser)
        return [permission() for permission in permissions_lst]

    def ban_user(self, *args, **kwargs):
        user = self.get_object()
        user.ban()
        return Response(data={'message': 'User has been banned'}, status=status.HTTP_200_OK)

    def unban_user(self, *args, **kwargs):
        user = self.get_object()
        user.unban()
        return Response(data={'message': 'User has been unbanned'}, status=status.HTTP_200_OK)


class ObtainTokensPairView(GenericAPIView):
    serializer_class = ObtainTokensPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ObtainAccessTokenView(GenericAPIView):
    serializer_class = ObtainAccessTokenSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

    
