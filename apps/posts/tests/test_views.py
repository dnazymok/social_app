from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp


class ListCreateViewTest(TestSetUp):
    def test_can_read_posts_list(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('posts:index'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'username')

    def test_cant_create_post_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('posts:index'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cant_create_post(self):
        response = self.client.post(reverse('posts:index'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
