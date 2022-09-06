from rest_framework import serializers

from projects.models import Project, Issue, Contributor, Comment
from django.contrib.auth.models import User


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


class ContributorSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Contributor
        fields = "__all__"
        extra_kwargs = {
            "role": {'read_only': True},
            "project": {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "issue": {'read_only': True},
            "author": {'read_only': True},
        }
