from django.db.models import Q
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from comment.views import PermissionMixin
from post.models import Post, PostImage, Rating, Like
from post.serializers import PostSerializer, PostImageSerializer, RatingSerializer, LikeSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')  # = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def liked(self, request, pk=None):
        likes = Like.objects.filter(author=request.user)
        pin_list = [like.pin for like in likes]
        serializer = PostSerializer(pin_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class PostImageView(generics.ListAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class LikeViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class RatingViewSet(ModelViewSet, PermissionMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
