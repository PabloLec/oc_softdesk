from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import *
from .serializers import *


class IsProjectManager(permissions.BasePermission):
    def is_project_manager(self, user, project):
        try:
            Project.objects.get(pk=project)
        except ObjectDoesNotExist:
            return True
        try:
            contributor = Contributor.objects.get(user=user, project=project)
        except ObjectDoesNotExist:
            return False

        if not contributor.is_manager:
            return False

        return True


class IsProjectManagerFromProjectView(IsProjectManager):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True

        project = view.kwargs["pk"]
        return self.is_project_manager(user=request.user, project=project)


class IsProjectManagerFromContributorView(IsProjectManager):
    def has_permission(self, request, view):
        if not view.action in ("create", "destroy"):
            return True

        project = view.kwargs["projects_pk"]
        return self.is_project_manager(user=request.user, project=project)


class IsAuthor(permissions.BasePermission):
    def is_author(self, content_type, pk, user):
        try:
            content = content_type.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return True

        if content.author != user:
            return False

        return True


class IsIssueAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True
        return self.is_author(content_type=Issue, pk=view.kwargs["pk"], user=request.user)


class IsCommentAuthor(IsAuthor):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True
        return self.is_author(content_type=Comment, pk=view.kwargs["pk"], user=request.user)
