from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories.user_factory import UserFactory
from .test_setup import TestSetUp
from ..models import Post, Like


class ListTest(APITestCase):
    def test_can_read_posts_list(self):
        response = self.client.get(reverse('posts:post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateTest(APITestCase):
    post_data = {
        'title': 'title',
        'description': 'description',
        'content': 'content'
    }

    def setUp(self):
        factory = UserFactory()
        user = factory.make_user()
        self.user = user

    def test_can_create_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('posts:post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'username')

    def test_cant_create_post_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('posts:post-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cant_create_post(self):
        response = self.client.post(reverse('posts:post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DetailViewTest(TestSetUp):
    def test_can_read_post_detail(self):
        response = self.client.get(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutTest(TestSetUp):
    def test_can_update_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}),
            self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_title')

    def test_unauthorized_user_cant_update_post(self):
        response = self.client.put(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}),
            self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PatchTest(TestSetUp):
    def test_can_partial_update_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}),
            self.partial_update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_title')

    def test_unauthorized_user_cant_partial_update_post(self):
        response = self.client.patch(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}),
            self.partial_update_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteTest(TestSetUp):
    def test_can_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cant_delete_post(self):
        response = self.client.delete(
            reverse('posts:post-detail', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeCreateTest(TestSetUp):
    def test_can_create_like(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('posts:post-like', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_user_cant_create_like(self):
        response = self.client.post(
            reverse('posts:post-like', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeDeleteTest(TestSetUp):
    def setUp(self):
        factory = UserFactory()
        user = factory.make_user()
        self.user = user
        self.post = Post.objects.create(author_id=self.user.id)
        like = Like.objects.create(post_id=self.post.id, user_id=self.user.id)
        self.post.likes.add(like)

    def test_can_delete_like(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('posts:post-dislike', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cant_delete_like(self):
        response = self.client.delete(
            reverse('posts:post-dislike', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
