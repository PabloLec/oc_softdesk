from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import *
from .serializers import *


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        project_protected_actions = isinstance(view.get_serializer(), ProjectSerializer) and view.action in (
            "update",
            "destroy",
        )
        user_protected_actions = isinstance(view.get_serializer(), ContributorSerializer) and view.action in (
            "create",
            "destroy",
        )
        if project_protected_actions or user_protected_actions:
            if user_protected_actions:
                project = view.kwargs["projects_pk"]
            else:
                project = view.kwargs["pk"]

            try:
                contributor = Contributor.objects.get(user=request.user, project=project)
            except ObjectDoesNotExist:
                return False

            if not contributor.is_manager:
                return False
        return True
