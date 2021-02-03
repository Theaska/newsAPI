import base64

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .token import AuthToken, RefreshToken

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, data):
        user = self.Meta.model.objects.create(
            username=data['username'],
            email=data['email'],
        )
        user.set_password(data['password'])
        user.save()
        return user

    class Meta:
        model = user_model
        fields = ('id', 'username', 'password', 'email')


class ObtainTokensPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = {}
        user = authenticate(**attrs)
        access_token = user.get_access_token()
        refresh_token = user.get_refresh_token()
        data['access'] = base64.b64encode(access_token.encode("utf-8"))
        data['refresh'] = base64.b64encode(refresh_token.encode("utf-8"))
        return data