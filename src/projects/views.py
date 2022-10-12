# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from projects.models import Project, Contributor, Issue, Comment
from projects.permissions import ProjectPermission, ContributorPermission, CommentPermission, \
    IssuePermission
from projects.serializer import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer


class ProjectView(ModelViewSet):
    permission_classes = [IsAuthenticated, ProjectPermission]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(contributor__user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(author=request.user)
        Contributor.objects.create(user=request.user,
                                   project=project,
                                   role='AUTHOR')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        message = f"Project <{instance.title}> has been deleted."
        self.perform_destroy(instance)
        return Response({"message": message}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ContributorView(ModelViewSet):
    permission_classes = [IsAuthenticated, ContributorPermission]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Contributor.objects.filter(project=kwargs['projects_pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not Contributor.objects.filter(user=request.data['user'], project=kwargs['projects_pk']).exists():
            project = get_object_or_404(Project, pk=kwargs['projects_pk'])
            user = get_object_or_404(User, pk=request.data['user'])
            serializer.save(user=user, project=project, role='CONTRIBUTOR')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = f"User ID{request.data['user']} has already been linked to the project."
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not(instance.role == "AUTHOR"):
            message = f"Contributor <{instance.user.username}> has been deleted."
            self.perform_destroy(instance)
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            message = f"Author cannot be deleted !"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class IssueView(ModelViewSet):
    permission_classes = [IsAuthenticated, IssuePermission]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Issue.objects.filter(project=kwargs['projects_pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = get_object_or_404(Project, pk=kwargs['projects_pk'])
        if Contributor.objects.filter(user_id=request.data['assignee'], project=project).exists():
            assignee = get_object_or_404(User, id=request.data['assignee'])
            serializer.save(author=request.user, project=project, assignee=assignee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = f"Assignee must be part of the project!"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        message = f"Issue <{instance.title}> has been deleted."
        self.perform_destroy(instance)
        return Response({"message": message}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        project = get_object_or_404(Project, pk=kwargs['projects_pk'])
        instance = self.get_object()
        if 'assignee' in request.data:
            if not Contributor.objects.filter(user_id=request.data['assignee'], project=project).exists():
                message = f"Assignee must be part of the project!"
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CommentView(ModelViewSet):
    permission_classes = [IsAuthenticated, CommentPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(issue=kwargs['issues_pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = get_object_or_404(Issue, pk=kwargs['issues_pk'])
        serializer.save(author=request.user, issue=issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        message = f"Comment <{instance.description}> has been deleted."
        self.perform_destroy(instance)
        return Response({"message": message}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
