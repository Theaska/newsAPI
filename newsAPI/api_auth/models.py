from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from api_auth.exceptions import CanNotBanned, CanNotUnbanned
from helpers.send_notification import send_notification


class CustomUser(AbstractUser):
    """
        User model with additional fields:
            email:                  user's email.
            is_banned:              True, if user has been banned. Banned user can not add comments.
            refresh_token_hash:     save only md5 hash of refresh user token for security.
            refresh_token_expire:   date and time when lifetime of refresh token ended.
    """
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
        """
            Update user's info about hash and expired time of refresh token 
        """
        self.refresh_token_hash = token.token_md5_hash.hexdigest()
        self.refresh_token_expire = token.expired_time
        self.save()

    def ban(self):
        """
            Ban user and send him email about that.
            If user has already banned raises CanNotBanned exception.
        """
        if not self.is_banned:
            self.is_banned = True
            self.save()
            send_notification(
                template_name='api_auth/notify_user_banned.html',
                subject=_('You have been banned'),
                context={'user': self},
                receivers=[self.email, ]
            )
        else:
            raise CanNotBanned(_('This user has already banned'))

    def unban(self):
        """
            Unban user and send him email about that.
            If user is not banned raises CanNotUnBanned exception.
        """
        if self.is_banned:
            self.is_banned = False
            self.save()
            send_notification(
                template_name='api_auth/notify_user_unbanned.html',
                subject=_('You have been unbanned'),
                receivers=[self.email, ],
                context={'user': self}
            )
        else:
            raise CanNotUnbanned(_('This user is not banned'))



