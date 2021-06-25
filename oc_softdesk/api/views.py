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
    permission_classes = (IsProjectManagerFromProjectView,)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = (IsProjectManagerFromContributorView,)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = kwargs["projects_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = {"message": "HTTP_405_METHOD_NOT_ALLOWED"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        try:
            if Contributor.objects.get(pk=kwargs["pk"]).user == request.user:
                response = {"message": "You cannot delete yourself."}
                return Response(response, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            pass
        return super(ContributorViewSet, self).destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["projects_pk"])


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsIssueAuthor,)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = kwargs["projects_pk"]
        request.data["author"] = request.user.pk
        request.data["assignee"] = request.user.pk
        request.POST._mutable = False
        return super(IssueViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = {"message": "HTTP_405_METHOD_NOT_ALLOWED"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = kwargs["projects_pk"]
        request.POST._mutable = False
        return super(IssueViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = kwargs["projects_pk"]
        request.POST._mutable = False
        return super(IssueViewSet, self).destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["projects_pk"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsCommentAuthor,)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue"] = kwargs["issues_pk"]
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(CommentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue"] = kwargs["issues_pk"]
        request.POST._mutable = False
        return super(CommentViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issues_pk"])
