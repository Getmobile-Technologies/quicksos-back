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
        
        
class IsAgent(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'agent')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
class IsEscalator(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'escalator') 
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        

class IsResponder(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'first_responder') 
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        

