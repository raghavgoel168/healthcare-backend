from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow owners to edit/delete only.
    Assumes the model instance has a `created_by` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for authenticated users (or change to allow anyone)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions: owner only
        return getattr(obj, 'created_by', None) == request.user
