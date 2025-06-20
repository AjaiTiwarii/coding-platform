from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors to edit their content.
    Works with models that have `created_by` or `user` field.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        # Check for common author field names
        author_field = getattr(obj, 'created_by', None) or getattr(obj, 'user', None)
        return author_field == request.user

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to modify content.
    All users can read, only admins can write.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsProblemCreatorOrAdmin(BasePermission):
    """
    Custom permission for problem management.
    Only problem creators or admins can modify problems.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return (
            request.user == obj.created_by or 
            request.user.is_staff
        )

class IsSubmissionOwner(BasePermission):
    """
    Custom permission for submission access.
    Users can only access their own submissions unless they're admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class CanJudgeSubmissions(BasePermission):
    """
    Permission for users who can judge submissions.
    Typically for staff members or designated judges.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'can_judge', False))
        )

class IsProfileOwner(BasePermission):
    """
    Custom permission for user profile access.
    Users can only modify their own profiles.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
