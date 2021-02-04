from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import permissions

from .serializers import UserSerializer, ObtainTokensPairSerializer, ObtainAccessTokenSerializer
from .token import AuthToken, RefreshToken


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permissions_classes = [
        permissions.NOT, permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer


class ObtainTokensPairView(GenericAPIView):
    serializer_class = ObtainTokensPairSerializer
    permissions_classes = [
        permissions.NOT, permissions.IsAuthenticated,
    ]

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

    
