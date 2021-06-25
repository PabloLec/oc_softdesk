from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import *


class IsAuthor(permissions.BasePermission):
    def is_author(self, content_type, pk, user):
        try:
            content = content_type.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return True

        print(content.author, user)
        if content.author != user:
            return False

        return True


class IsProjectAuthorFromProjectView(IsAuthor):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True

        return self.is_author(content_type=Project, pk=view.kwargs["pk"], user=request.user)


class IsProjectAuthorFromContributorView(IsAuthor):
    def has_permission(self, request, view):
        if not view.action in ("create", "destroy"):
            return True

        return self.is_author(content_type=Project, pk=view.kwargs["projects_pk"], user=request.user)


class IsIssueAuthor(IsAuthor):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True
        return self.is_author(content_type=Issue, pk=view.kwargs["pk"], user=request.user)


class IsCommentAuthor(IsAuthor):
    def has_permission(self, request, view):
        if not view.action in ("update", "destroy"):
            return True
        return self.is_author(content_type=Comment, pk=view.kwargs["pk"], user=request.user)


class IsContributor(permissions.BasePermission):
    def is_contributor(self, user, project):
        try:
            Contributor.objects.get(user=user, project=project)
        except ObjectDoesNotExist:
            return False

        return True


class IsContributorFromProjectView(IsContributor):
    def has_permission(self, request, view):
        if view.action in ("list", "create"):
            return True

        return self.is_contributor(user=request.user, project=view.kwargs["pk"])


class IsContributorFromIssueAndCommentView(IsContributor):
    def has_permission(self, request, view):
        return self.is_contributor(user=request.user, project=view.kwargs["projects_pk"])
