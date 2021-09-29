from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', 'username']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'date_posted', 'author']
