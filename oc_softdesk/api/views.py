from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *
from .permissions import *


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsProjectManager,)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    http_method_names = ["get", "post", "delete"]

    def retrieve(self, request, projects_pk=None, pk=None):
        response = {"message": "HTTP_405_METHOD_NOT_ALLOWED"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["projects_pk"])


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def retrieve(self, request, projects_pk=None, pk=None):
        response = {"message": "HTTP_405_METHOD_NOT_ALLOWED"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["projects_pk"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issues_pk"])
