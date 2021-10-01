from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from apps.posts.models import Post


class TestSetUp(APITestCase):
    def setUp(self):
        User.objects.create_user(username='username',
                                 email='email@gmail.com',
                                 password='password')
        self.user = User.objects.get(username='username')
        self.post = Post.objects.create(author_id=self.user.id)
        self.update_post_data = {'title': 'new_title',
                                 'description': 'new_description',
                                 'content': 'new_content'}
        self.partial_update_post_data = {'title': 'new_title',
                                         'description': 'new_description'}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
