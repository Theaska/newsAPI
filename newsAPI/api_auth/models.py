import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email'), unique=True)
    refresh_token_hash = models.CharField(max_length=256, blank=True, null=True)
    refresh_token_expire = models.DateTimeField(blank=True, null=True)

    def get_access_token(self):
        from .token import AuthToken
        return AuthToken(self).token

    def get_refresh_token(self):
        from .token import RefreshToken
        refresh_token = RefreshToken()
        self.refresh_token_hash = hashlib.md5(refresh_token.token.encode("utf-8"))
        self.refresh_token_expire = refresh_token.expired_time
        return refresh_token.token

