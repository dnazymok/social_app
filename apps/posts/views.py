from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db import IntegrityError
from django.http import Http404

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


class LikeCreateDeleteView(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericAPIView):
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'IntegrityError'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        try:
            return Like.objects.get(user_id=self.request.user.id,
                                    post_id=self.kwargs.get('pk'))
        except Like.DoesNotExist:
            raise Http404

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Like.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))
