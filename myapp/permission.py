from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacher(BasePermission):
    """
        Only teachers can access this endpoint. No one else gets in.
    """

    messae = "You must be teacher to perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )
    
class IsStudent(BasePermission):
    """
    Only student can access this point
    """
    message = "you must be student to perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'student'
        )
    
class IsTeacherOrReadOnly(BasePermission):
    """
    Teachers can do anything.
    Students / unauthenticated users can only READ (GET,HEAD, OPTIONS).
    """

    message = "only teacher can modifly this"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )
    
class IsEnrolledStudent(BasePermission):
    """
    Only students enrolled in the specific course can access lessons
    """
    message = "you must be enrolled in this course"

    def has_object_permission(self, request, view, obj):
        from .models import Enrollment
        return Enrollment.object.filter(
            students = request.user, course=obj.course).exsists()
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Only the teacher who created the course can edit/delete it.
    Others can only read.
    """
    message = "You must be the owner of this resource."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.teacher == request.user