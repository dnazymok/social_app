from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from apps.posts.models import Post
from apps.posts.tests.factories.user_factory import UserFactory


class TestSetUp(APITestCase):
    def setUp(self):
        factory = UserFactory()
        user = factory.make_user()
        self.user = user
        self.post = Post.objects.create(author_id=self.user.id)
        self.update_post_data = {
            'title': 'new_title',
            'description': 'new_description',
            'content': 'new_content'
        }
        self.partial_update_post_data = {
            'title': 'new_title',
            'description': 'new_description'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
