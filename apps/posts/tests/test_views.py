from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from ..models import Post, Like


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


class DetailViewTest(TestSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('posts:index'), self.post_data)
        self.client.logout()

    def test_can_read_post_detail(self):
        pk = Post.objects.first().id
        response = self.client.get(reverse('posts:detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_post(self):
        pk = Post.objects.first().id
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('posts:detail', kwargs={'pk': pk}),
                                   self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_title')

    def test_unauthorized_user_cant_update_post(self):
        pk = Post.objects.first().id
        response = self.client.put(reverse('posts:detail', kwargs={'pk': pk}),
                                   self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_partial_update_post(self):
        pk = Post.objects.first().id
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse('posts:detail', kwargs={'pk': pk}),
            self.partial_update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_title')

    def test_unauthorized_user_cant_partial_update_post(self):
        pk = Post.objects.first().id
        response = self.client.patch(
            reverse('posts:detail', kwargs={'pk': pk}),
            self.partial_update_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_post(self):
        pk = Post.objects.first().id
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('posts:detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cant_delete_post(self):
        pk = Post.objects.first().id
        response = self.client.delete(
            reverse('posts:detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeCreateDeleteViewTest(TestSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('posts:index'), self.post_data)
        self.client.logout()

    def test_can_create_like(self):
        pk = Post.objects.first().id
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('posts:likes', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_user_cant_create_like(self):
        pk = Post.objects.first().id
        response = self.client.post(
            reverse('posts:likes', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_like(self):
        post = Post.objects.first()
        pk = post.id
        like = Like.objects.create(post_id=pk, user_id=self.user.id)
        post.likes.add(like)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('posts:likes', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cant_delete_like(self):
        pk = Post.objects.first().id
        response = self.client.delete(
            reverse('posts:likes', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
