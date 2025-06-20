from rest_framework.permissions import BasePermission

class IsSubmissionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
