from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CreateTest(APITestCase):
    valid_data = {
        'username': 'username',
        'email': 'email@gmail.com',
        'password': 'password'
    }
    invalid_data = {
        'username': 'username',
        'email': 'email',
        'password': 'password'
    }

    def test_can_create_user(self):
        response = self.client.post(reverse('users:index'), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'username')

    def test_cant_create_user_with_invalid_data(self):
        response = self.client.post(reverse('users:index'), self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
