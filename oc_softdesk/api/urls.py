from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_jwt.views import obtain_jwt_token
from . import views

projects_router = routers.SimpleRouter()
projects_router.register(r"projects", views.ProjectViewSet)

users_router = routers.NestedSimpleRouter(projects_router, r"projects", lookup="projects")
users_router.register(r"users", views.ContributorViewSet, basename="users")

issues_router = routers.NestedSimpleRouter(projects_router, r"projects", lookup="projects")
issues_router.register(r"issues", views.IssueViewSet, basename="issues")

comments_router = routers.NestedSimpleRouter(issues_router, r"issues", lookup="issues")
comments_router.register(r"comments", views.CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(projects_router.urls)),
    path("", include(users_router.urls)),
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
    path("login", obtain_jwt_token),
]
