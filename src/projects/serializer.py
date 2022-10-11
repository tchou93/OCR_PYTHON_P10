from rest_framework import serializers
from projects.models import Project, Issue, Contributor, Comment
from users.serializer import UserSerializer
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author', 'id']
        extra_kwargs = {
            'author': {'read_only': True},
            'id': {'read_only': True}
        }

    def get_author(self, obj):
        customer_account_query = User.objects.get(pk=obj.author_id)
        serialize = UserSerializer(customer_account_query)
        return serialize.data


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'project',
                  'status', 'author', 'assignee', 'created_time', 'id']
        extra_kwargs = {
            'author': {'read_only': True},
            'project': {'read_only': True},
            'created_time': {'read_only': True},
            'id': {'read_only': True}
        }


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role', 'id']
        extra_kwargs = {
            'role': {'read_only': True},
            'project': {'read_only': True},
            'id': {'read_only': True}
        }

    def get_user(self, obj):
        customer_account_query = User.objects.get(pk=obj.user_id)
        serialize = UserSerializer(customer_account_query)
        return serialize.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time', 'id']
        extra_kwargs = {
            'issue': {'read_only': True},
            'author': {'read_only': True},
            'created_time': {'read_only': True},
            'id': {'read_only': True}
        }
