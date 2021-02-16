from rest_framework.permissions import BasePermission


class IsNotBanned(BasePermission):
    """
        Allows access only to not banned users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_banned)
