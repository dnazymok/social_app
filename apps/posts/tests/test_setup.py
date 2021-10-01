from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username='username',
                                 email='email@gmail.com',
                                 password='password')
        self.user = User.objects.get(username='username')
        self.post_data = {'title': 'title', 'description': 'description',
                          'content': 'content'}
        return super().setUp()
