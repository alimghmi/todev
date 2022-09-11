from django.db.models import Q
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectCustomPermission(BasePermission):
    """
    Custom permission class to check if user is a project manager or
    a member of project who is accessing the objects via safe methods

    behaviors:
        - Super user has full control
        - Allow any authinticated user to init a new project
        - Owner(project manager) has full control
        - Readonly access for members(developers)
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: 
            return True

        if request.method in ['POST']: 
            return True

        if obj.owner == request.user: 
            return True

        if request.method in SAFE_METHODS: 
            return obj.__class__.objects.filter(pk=obj.id, members__in=[request.user]).exists()

        return False


class TaskCustomPermission(BasePermission):
    """
    Custom permission class to check if user is an author of a task
    or a project manager

    behaviors:
        - Super user has full control
        - Owner(project manager) has full control
        - Author(PM or DEV who created the task) has full control
        - Readonly access for members
        - Assignees has partial control, they can't delete a task
          but they can update the fields such as status
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: 
            return True

        if obj.project.owner == request.user:
            return True

        if obj.author == request.user: 
            return True

        if request.method in SAFE_METHODS:
            return obj.project.members.filter(pk=request.user.id).exists()

        if request.method not in ('DELETE'):
            return obj.__class__.objects.filter(pk=obj.id, assignees__in=[request.user]).exists()
        
        return False