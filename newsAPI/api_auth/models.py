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
        return AuthToken(self)

    def get_refresh_token(self):
        from .token import RefreshToken
        return RefreshToken(self)
    
    def update_refresh_token(self, token):
        self.refresh_token_hash = token.token_md5_hash.hexdigest()
        self.refresh_token_expire = token.expired_time
        self.save()
        

