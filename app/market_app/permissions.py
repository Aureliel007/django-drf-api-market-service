from rest_framework import permissions


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role == user.ROLE_CHOICES[1][0])

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.shop.user == request.user) or request.user.is_staff
    
class IsBasketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user