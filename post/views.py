from django.db.models import Q
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comment.views import PermissionMixin
from post.models import Post, PostImage, Saved, Rating
from post.serializers import PostSerializer, PostImageSerializer, SavedSerializer, RatingSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['POST'])
    def saved(self, requests, *args, **kwargs):
        post = self.get_object()
        saved_obj, _ = Saved.objects.get_or_create(post=post, user=requests.user)
        saved_obj.saved = not saved_obj.saved
        saved_obj.save()
        status = 'Сохранено в избранные'
        if not saved_obj.saved:
            status = 'Удалено из избранных'
        return Response({'status': status})

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')  # = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class SavedView(generics.ListAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer


class RatingViewSet(ModelViewSet, PermissionMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
