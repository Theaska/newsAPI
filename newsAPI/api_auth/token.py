import hashlib
import base64

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import jwt

from .exceptions import TokenException

UserModel = get_user_model()


ALGORITHMS = (
    "HS256",
    "HS384",
    "HS512",
    "PS256",
    "PS384",
    "PS512",
    "RS256",
    "RS384",
    "RS512",
    "ES256",
    "ES256K",
    "ES384",
    "ES512",
    "EdDSA",
)


class Token:
    algorithm = "HS256"
    lifetime = 60*60

    def __init__(self, algorithm=None, lifetime=None):
        self._validate_algorithm(algorithm)
        self.algorithm = algorithm
        self._expired_time, self._token = self._generate_token()
        
    def _validate_algorithm(self, algorithm):
        if algorithm not in ALGORITHMS:
            raise TokenException('algorithm {} is not valid'.format(algorithm))

    def _generate_token(self):
        expired_time = timezone.now() + timezone.timedelta(seconds=self.lifetime)
        payload = self.get_payload()
        payload['expired_time'] = expired_time.timestamp()
        return expired_time, jwt.encode(payload, key=settings.SECRET_KEY, algorithm=self.algorithm)

    def get_payload(self):
        return {}
    
    def check_expire_time(self):
        if timezone.now().timestamp() > self.expired_tome.timestamp():
            return False
        else:
            return True
    
    @property
    def token_md5_hash(self):
        return hashlib.md5(self.token.encode('utf-8'))
    
    @property
    def b64_encoded_token(self):
        return base64.b64encode(self.token.encode("utf-8"))
    
    @classmethod
    def decode_token(cls, token):
        return jwt.decode(token, key=settings.SECRET_KEY, algorithms=(cls.algorithm))

    @property
    def token(self):
        return self._token

    @property
    def expired_time(self):
        return self._expired_time
    
    def __str__(self):
        return str(self.token)


class UserTokenMixin:
    def __init__(self, user):
        self.user = user
        super().__init__()

    def get_payload(self):
        payload = super().get_payload()
        payload['user'] = self.user.id
        return payload


class AuthToken(UserTokenMixin, Token):
    lifetime = settings.ACCESS_TOKEN_LIFETIME


class RefreshToken(UserTokenMixin, Token):
    lifetime = settings.REFRESH_TOKEN_LIFETIME
