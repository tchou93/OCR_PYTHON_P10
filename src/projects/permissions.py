from rest_framework.permissions import BasePermission, SAFE_METHODS

from projects.models import Project, Contributor

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return Contributor.objects.filter(user=request.user).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "DELETE"]:
            return request.user == obj.author
        else:
            return Contributor.objects.filter(user=request.user).filter(project=obj.id).exists()

class IssueOrCommentPermission(BasePermission):
    def has_permission(self, request, view):
        return Contributor.objects.filter(user=request.user).filter(project=view.kwargs['projects_pk']).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "DELETE"]:
            return request.user == obj.author
        else:
            return Contributor.objects.filter(user=request.user).filter(project=view.kwargs['projects_pk']).exists()

class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        if Contributor.objects.filter(user=request.user).filter(project=view.kwargs['projects_pk']).exists():
            if request.method in SAFE_METHODS:
                return True
            else:
                return Project.objects.filter(id=view.kwargs['projects_pk']).filter(author=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "DELETE"]:
            return Project.objects.filter(id=view.kwargs['projects_pk']).filter(author=request.user).exists()
        else:
            return False