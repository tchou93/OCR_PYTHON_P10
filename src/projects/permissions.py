from rest_framework.permissions import BasePermission

from projects.models import Project, Contributor, Issue, Comment


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        # get all the projects
        if request.method in ["GET"]:
            return Contributor.objects.filter(user=request.user).exists()
        # create the project
        elif request.method in ["POST"]:
            return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Update or delete a project
        if request.method in ["PUT", "DELETE"]:
            return request.user == obj.author
        # get the detail of a project
        elif request.method in ["GET"]:
            return Contributor.objects.filter(user=request.user, project=obj.id).exists()
        else:
            return False


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        # get all the Contributors
        if request.method in ["GET"]:
            return Contributor.objects.filter(user=request.user, project=view.kwargs['projects_pk']).exists()
        # Add a contributor to a project
        elif request.method in ["POST"]:
            return Project.objects.filter(id=view.kwargs['projects_pk'], author=request.user).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Delete a contributor from a project
        if request.method in ["DELETE"]:
            return Project.objects.filter(id=view.kwargs['projects_pk'], author=request.user).exists()
        else:
            return False


class IssuePermission(BasePermission):
    def has_permission(self, request, view):
        # "get all the issues concerning a project" or "create an issue to a project"
        if request.method in ["GET", "POST"]:
            return Contributor.objects.filter(user=request.user, project=view.kwargs['projects_pk']).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Update or delete an issue from a project
        if request.method in ["PUT", "DELETE"]:
            return (request.user == obj.author) and \
                   Issue.objects.filter(project=view.kwargs['projects_pk'], id=obj.id).exists()
        else:
            return False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        # "get all the comments concerning an issue"
        if request.method in ["GET"]:
            return Contributor.objects.filter(user=request.user, project=view.kwargs['projects_pk']).exists()
        # "create a comment to an issue"
        if request.method in ["POST"]:
            return Issue.objects.filter(project=view.kwargs['projects_pk'], id=view.kwargs['issues_pk']).exists() and \
                   Contributor.objects.filter(user=request.user, project=view.kwargs['projects_pk']).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Update or delete a comment
        if request.method in ["PUT", "DELETE"]:
            return (request.user == obj.author) and \
                   Comment.objects.filter(issue=view.kwargs['issues_pk'], id=obj.id).exists() and \
                   Issue.objects.filter(project=view.kwargs['projects_pk'], id=view.kwargs['issues_pk']).exists()
        # get the detail of a comment
        elif request.method in ["GET"]:
            return Contributor.objects.filter(user=request.user, project=view.kwargs['projects_pk']).exists()
        else:
            return False
