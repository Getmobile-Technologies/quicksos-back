from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'admin')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")