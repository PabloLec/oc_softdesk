from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from .serializers import *
from .models import *
from .permissions import *


@permission_classes([])
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }
        )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (
        IsProjectAuthorFromProjectView,
        IsContributorFromProjectView,
    )

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = (
        IsProjectAuthorFromContributorView,
        IsContributor,
    )

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
    permission_classes = (
        IsIssueAuthor,
        IsContributorFromIssueAndCommentView,
    )

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
    permission_classes = (
        IsCommentAuthor,
        IsContributorFromIssueAndCommentView,
    )

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
