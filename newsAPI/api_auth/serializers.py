import base64
import hashlib
import binascii

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from jwt import exceptions

from .token import RefreshToken

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for creating/signup new user """
    is_banned = serializers.ReadOnlyField()
    
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
        fields = ('id', 'username', 'password', 'email', 'is_banned')


class ObtainTokensPairSerializer(serializers.Serializer):
    """ Serializer for creating new access and refresh tokens after authentication """
    
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = {}
        
        # trying to get user
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError(_('Wrong username or password'))
        
        # if user exists returns access token and refresh token
        access_token = user.get_access_token()
        refresh_token = user.get_refresh_token()
        
        # also save hash of refresh token in db
        user.update_refresh_token(refresh_token)
        
        data['access'] = access_token.b64_encoded_token
        data['refresh'] = refresh_token.b64_encoded_token
        return data


class ObtainAccessTokenSerializer(serializers.Serializer):
    """ Serializer for creating new pairs of access and refresh tokens using refresh token """
    
    refresh_token = serializers.CharField()

    def validate(self, data):
        encoded_token = data.get('refresh_token')
        try:
            token = base64.b64decode(encoded_token)
        except binascii.Error:
            raise serializers.ValidationError(_('Can not decode refresh token'))
        
        try:
            decoded_token = RefreshToken.decode_token(token)
            user_id = decoded_token.get('user')
        except exceptions.DecodeError:
            raise serializers.ValidationError(_('Can not decode refresh token'))
        
        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            raise serializers.ValidationError(_('Can not find user with refresh token'))
        
        # compare hash refresh token from request with hash RT in DB
        if not user.refresh_token_hash == hashlib.md5(token).hexdigest():
            raise serializers.ValidationError(_('Invalid refresh token for user'))
        
        # check if time is ended
        if not self.validate_exp_time(decoded_token):
            raise serializers.ValidationError(_('Lifetime of your refresh token'))
        else:
            access_token = user.get_access_token()
            refresh_token = user.get_refresh_token()
            user.update_refresh_token(refresh_token)
            return {
                'access_token': access_token.b64_encoded_token,
                'refresh_token': refresh_token.b64_encoded_token,
            }
    
    def validate_exp_time(self, token):
        if timezone.now().timestamp() > token['expired_time']:
            return False
        else:
            return True



