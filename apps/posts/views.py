from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .serializers import PostSerializer
from .models import Post


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
