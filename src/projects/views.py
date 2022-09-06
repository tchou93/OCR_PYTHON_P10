# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from projects.models import Project, Contributor, Issue, Comment
from projects.permissions import ProjectPermission, ContributorPermission, IssueOrCommentPermission
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
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author=request.user)
            Contributor.objects.create(user=request.user,
                                       project=project,
                                       role='AUTHOR')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        project = Project.objects.get(id=kwargs['projects_pk'])
        serializer = ContributorSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(id=request.data['user'])
            serializer.save(user=user, project=project, role='CONTRIBUTOR')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueView(ModelViewSet):
    permission_classes = [IsAuthenticated, IssueOrCommentPermission]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def list(self, request, *args, **kwargs):
        projects_pk = kwargs['projects_pk']
        queryset = Issue.objects.filter(project=projects_pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['projects_pk'])
        serializer = IssueSerializer(data=request.data)
        assignee = User.objects.get(id=request.data['assignee'])
        if serializer.is_valid():
            serializer.save(author=request.user, project=project, assignee=assignee)
            # serializer.save(author=request.user, project=project, assignee=assignee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(ModelViewSet):
    permission_classes = [IsAuthenticated, IssueOrCommentPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(issue=kwargs['issues_pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        issue = Issue.objects.get(id=kwargs['issues_pk'])
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, issue=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
