from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

import jwt


UserModel = get_user_model()

class Token:
    algorithm = "HS256"
    lifetime = 60*60

    def __init__(self):
        self._expired_time, self._token = self._generate_token()

    def _generate_token(self):
        expired_time = timezone.now() + timezone.timedelta(seconds=self.lifetime)
        payload = self.get_payload()
        payload['expired_time'] = expired_time.timestamp()
        return expired_time, jwt.encode(payload, key=settings.SECRET_KEY, algorithm=self.algorithm)

    def get_payload(self):
        return {}
    
    @classmethod
    def decode_token(cls, token):
        return jwt.decode(token, key=settings.SECRET_KEY)

    @property
    def token(self):
        return self._token

    @property
    def expired_time(self):
        return self._expired_time


class AuthToken(Token):
    lifetime = settings.ACCESS_TOKEN_LIFETIME

    def __init__(self, user):
        self.user = user
        super().__init__()

    def get_payload(self):
        payload = super().get_payload()
        payload.update({
            'user': self.user.id,
        })
        return payload


class RefreshToken(Token):
    lifetime = settings.REFRESH_TOKEN_LIFETIME
