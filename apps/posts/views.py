from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.generics import GenericAPIView

from .serializers import PostSerializer
from .models import Post


class ListView(mixins.ListModelMixin, GenericAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

