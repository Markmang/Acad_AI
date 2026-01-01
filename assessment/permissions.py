from rest_framework.permissions import BasePermission

class IsExamOwner(BasePermission):
    """
    Allows access only to the staff who created the exam.
    Superuser automatically has full access.
    """
    def has_object_permission(self, request, view, obj):

        # Superuser bypass
        if request.user and request.user.is_superuser:
            return True

        return obj.created_by == request.user

# A student can ONLY view their own submission
class IsSubmissionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user
