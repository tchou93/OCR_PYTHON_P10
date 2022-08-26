# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project, Contributor, Issue
from projects.serializer import ProjectSerializer, IssueSerializer


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(contributor__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            print("ici")
            project = serializer.save(author=request.user)
            Contributor.objects.create(user=request.user,
                                       project=project,
                                       role='AUTHOR')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Issue.objects.filter(project=2)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=4)
        serializer = IssueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
