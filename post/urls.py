from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet, RatingViewSet, LikeViewSet

router = DefaultRouter()
router.register('ratings', RatingViewSet)
router.register('likes', LikeViewSet)
router.register('', PostViewSet)
urlpatterns = [
    path('', include(router.urls)),
]