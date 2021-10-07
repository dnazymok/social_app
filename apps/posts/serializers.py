from rest_framework import serializers
from .models import Post, Like


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    count_of_likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'date_posted',
                  'author', 'count_of_likes']

    def get_count_of_likes(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user']