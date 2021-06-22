from rest_framework import permissions

from .models import *


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ("update", "destroy"):
            project = view.kwargs["pk"]
            contributor = Contributor.objects.get(user=request.user, project=project)
            if not contributor.is_manager:
                return False
        return True
