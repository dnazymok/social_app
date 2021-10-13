from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


class Post(TimeStampedModel):
    title = models.TextField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
