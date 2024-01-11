from rest_framework import permissions

from .models import Advertiser


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or "advertiser" not in request.data:
            return True
        return request.user == Advertiser.objects.get(pk=request.data["advertiser"]).owner
    
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.advertiser.owner == request.user
    
