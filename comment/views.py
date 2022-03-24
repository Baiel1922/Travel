from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsActivePermission
from .models import Comment
from .permissions import IsAuthorPermission
from .serializers import CommentSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == "create":
            permissions = [IsActivePermission]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthorPermission]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

