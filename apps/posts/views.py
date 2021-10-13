from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        like = Like()
        post = self.get_object()
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            like.post = post
            like.user = request.user
            like.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['delete'])  # todo or 1 action post/delete
    def dislike(self, request, pk=None):
        like = Like.objects.get(
            user_id=self.request.user.id,
            post_id=self.kwargs.get('pk')
        )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
