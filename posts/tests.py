from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

User = get_user_model()


class PostViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username='author',
            password='test-password',
            email='author@example.com',
        )
        cls.other_user = User.objects.create_user(
            username='other',
            password='test-password',
            email='other@example.com',
        )

    def test_create_post_requires_authentication(self):
        response = self.client.get(
            reverse('posts:post_create')
        )

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next='
            f'{reverse("posts:post_create")}',
        )

    def test_authenticated_user_can_create_post(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('posts:post_create'),
            {
                'topic': 'New post',
                'content': 'This is a new post.',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        post = Post.objects.get(topic='New post')

        self.assertEqual(post.author, self.author)
        self.assertEqual(post.content, 'This is a new post.')

    def test_author_can_edit_own_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Original topic',
            content='Original content',
        )

        self.client.force_login(self.author)

        response = self.client.get(
            reverse(
                'posts:post_update',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_cannot_edit_foreign_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Original topic',
            content='Original content',
        )

        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                'posts:post_update',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_anonymous_user_cannot_edit_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Original topic',
            content='Original content',
        )

        response = self.client.get(
            reverse(
                'posts:post_update',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next='
            f'{reverse("posts:post_update", kwargs={"post_id": post.pk})}',
        )

    def test_author_can_delete_own_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Topic',
            content='Some content',
        )

        self.client.force_login(self.author)

        response = self.client.post(
            reverse(
                'posts:post_delete',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse('posts:post_list'),
        )

        self.assertFalse(
            Post.objects.filter(pk=post.pk).exists()
        )

    def test_user_cannot_delete_foreign_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Topic',
            content='Some content',
        )

        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                'posts:post_delete',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        self.assertTrue(
            Post.objects.filter(pk=post.pk).exists()
        )

    def test_anonymous_user_cannot_delete_post(self):
        post = Post.objects.create(
            author=self.author,
            topic='Topic',
            content='Some content',
        )

        response = self.client.get(
            reverse(
                'posts:post_delete',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next='
            f'{reverse("posts:post_delete", kwargs={"post_id": post.pk})}',
        )

    def test_post_list_is_paginated(self):
        Post.objects.bulk_create(
            [
                Post(
                    author=self.author,
                    topic=f'Topic {index}',
                    content=f'Content {index}',
                )
                for index in range(11)
            ]
        )

        response = self.client.get(
            reverse('posts:post_list')
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.context['post_list']),
            10,
        )
        self.assertTrue(
            response.context['page_obj'].has_next()
        )

    def test_post_detail_is_available(self):
        post = Post.objects.create(
            author=self.author,
            topic='Test topic',
            content='Test post content',
        )

        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': post.pk},
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['object'], post)

    def test_post_list_is_ordered_by_newest_first(self):
        first_post = Post.objects.create(
            author=self.author,
            topic='First post',
            content='First post content',
        )

        second_post = Post.objects.create(
            author=self.author,
            topic='Second post',
            content='Second post content',
        )

        second_post.created_at = first_post.created_at + timedelta(minutes=1)
        second_post.save(update_fields=['created_at'])

        response = self.client.get(
            reverse('posts:post_list')
        )

        posts = list(response.context['post_list'])

        self.assertEqual(posts[0], second_post)
        self.assertEqual(posts[1], first_post)

    def test_post_form_rejects_empty_content(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('posts:post_create'),
            {
                'topic': 'Test post',
                'content': '',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(
            Post.objects.filter(topic='Test post').exists()
        )

    def test_post_form_rejects_short_content(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('posts:post_create'),
            {
                'topic': 'Test post',
                'content': 'Short',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFalse(
            Post.objects.filter(topic='Test post').exists()
        )
