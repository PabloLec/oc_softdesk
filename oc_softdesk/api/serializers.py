from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "project_type")


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ("user", "project", "is_manager")


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ("title", "description", "project", "author", "assignee", "tag", "priority", "status")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("description", "author", "issue")