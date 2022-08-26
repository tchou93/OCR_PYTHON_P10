from rest_framework import serializers

from projects.models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "author": {'read_only': True},
        }

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        extra_kwargs = {
            "author": {'read_only': True},
            "project": {'read_only': True},
        }