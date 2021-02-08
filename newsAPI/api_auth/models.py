from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email'), unique=True)
    is_banned = models.BooleanField(_('banned'), default=False)
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

    def ban(self):
        if not self.is_banned:
            self.is_banned = True
            self.save()
            send_notification()

    def unban(self):
        if self.is_banned:
            self.is_banned = False
            self.save()
            send_notification()


def send_notification():
    pass
