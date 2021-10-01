from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CreateTest(APITestCase):
    user_data = {
        'username': 'username',
        'email': 'email@gmail.com',
        'password': 'password'
    }

    def test_can_create_user(self):
        response = self.client.post(reverse('users:index'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'username')
