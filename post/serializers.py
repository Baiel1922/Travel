from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from account.models import User
from comment.serializers import CommentSerializer
from post.models import Post, PostImage, Saved, Rating
from post.utils import get_rating


class SavedSerializer(ModelSerializer):
    class Meta:
        model = Saved
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation["comments"] = CommentSerializer(instance.comments.all(), many=True).data
        representation['rating'] = get_rating(representation.get('id'), Post)

        return representation


class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        pin = validated_data.get('pin')

        if Rating.objects.filter(author=user, pin=pin):
            rating = Rating.objects.get(author=user, pin=pin)
            return rating

        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating


class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
