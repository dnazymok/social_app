from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class ListCreateView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DetailView(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LikeListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         GenericAPIView):
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Like.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))


class LikeDeleteView(mixins.DestroyModelMixin,
                     GenericAPIView):
    serializer_class = LikeSerializer
    lookup_field = 'user_id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        return Like.objects.filter(post_id=post_id, user_id=user_id)
