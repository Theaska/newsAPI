from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import permissions

from .exceptions import CanNotBanned, CanNotUnbanned
from .serializers import UserSerializer, ObtainTokensPairSerializer, ObtainAccessTokenSerializer


class UserViewSet(ModelViewSet):
    """
        ModelViewSet for:
            1. getting list of users (for Admin user),
            2. creating new user,
            3. getting information about user with selected user id (for Admin user),
            4. ban user with selected user id (for Admin user),
            5. unban user with selected user id (for Admin user).

    """
    model = get_user_model()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def get_permissions(self):
        permissions_lst = []
        if self.action in ('list', 'ban_user', 'retrieve'):
            permissions_lst.append(permissions.IsAdminUser)
        return [permission() for permission in permissions_lst]

    def ban_user(self, *args, **kwargs):
        """ Ban user with user_id getting from request params. """
        user = self.get_object()
        try:
            user.ban()
        except CanNotBanned as e:
            message = str(e)
        else:
            message = _('User has been banned')
        return Response(data={'message': message}, status=status.HTTP_200_OK)

    def unban_user(self, *args, **kwargs):
        """ Unan user with user_id getting from request params. """
        user = self.get_object()
        try:
            user.unban()
        except CanNotUnbanned as e:
            message = str(e)
        else:
            message = _('User has been unbanned')
        return Response(data={'message': message}, status=status.HTTP_200_OK)


class ObtainTokensPairView(GenericAPIView):
    """
        View for obtaining access and refresh token for user.
    """
    serializer_class = ObtainTokensPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ObtainAccessTokenView(GenericAPIView):
    """
        View for updating access and refresh token using old refresh token.
    """
    serializer_class = ObtainAccessTokenSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

    
