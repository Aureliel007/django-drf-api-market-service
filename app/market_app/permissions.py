from rest_framework import permissions


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role == user.ROLE_CHOICES[1][0])