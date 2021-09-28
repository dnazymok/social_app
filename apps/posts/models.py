from django.db import models
from apps.users.models import User


class Post(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
