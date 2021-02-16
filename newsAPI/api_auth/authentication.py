import base64
import binascii

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, exceptions
from jwt import exceptions as jwt_exceptions

from .token import AuthToken

UserModel = get_user_model()


class TokenAuthentication(BaseAuthentication):
    """
        Authentication class for getting user with using JWT.
    """
    def authenticate(self, request):
        headers = request.headers
        header_auth_key = self.authenticate_header(request)
        encoded_token = headers.get(header_auth_key)
        if encoded_token:
            token = self.encode_and_get_token(encoded_token)
            return self.get_user(token), token

    def encode_and_get_token(self, encoded_token):
        """
            Encode token from header and check it.
        """
        # check if token can be decoded
        try:
            b64_decoded = base64.b64decode(encoded_token)
        except binascii.Error:
            raise exceptions.AuthenticationFailed(_('Could not decode access token'))

        try:
            decoded_token = AuthToken.decode_token(b64_decoded)
        except jwt_exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(_('Invalid access token'))      
            
        # check token lifetime
        expired_time = decoded_token.get('expired_time')
        if timezone.now().timestamp() > expired_time:
            raise exceptions.AuthenticationFailed(_('Lifetime of access token is ended. Please, update your token'))

        return decoded_token

    def get_user(self, token):
        """
            Get user id from token and return user object
        """
        user_id = token.get('user')
        try:
            user = UserModel.objects.get(pk=user_id)
            return user
        except UserModel.DoesNotExists():
            raise exceptions.AuthenticationFailed(_('User not found'))

    def authenticate_header(self, request):
        return getattr(settings, 'HEADER_TOKEN_NAME', 'ACCESS-TOKEN')
