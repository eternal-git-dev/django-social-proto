from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test-user',
            password='test-password',
            email='test@example.com',
        )

    def test_registration_page_is_available(self):
        response = self.client.get(
            reverse('users:registration')
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            'users/registration.html',
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'new-user',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.assertTrue(
            User.objects.filter(
                username='new-user'
            ).exists()
        )

    def test_user_can_register_with_profile_data(self):
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'new-user',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'bio': 'Test biography',
                'date_of_birth': '2000-01-01',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        user = User.objects.get(username='new-user')

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.bio, 'Test biography')
        self.assertEqual(
            user.date_of_birth.isoformat(),
            '2000-01-01',
        )

    def test_registration_rejects_duplicate_email(self):
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'another-user',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': self.user.email,
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertFalse(
            User.objects.filter(
                username='another-user'
            ).exists()
        )

    def test_registration_rejects_invalid_email(self):
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'new-user',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'invalid-email',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertFalse(
            User.objects.filter(
                username='new-user'
            ).exists()
        )

    def test_registration_rejects_future_birth_date(self):
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'new-user',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'date_of_birth': '2099-01-01',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertFalse(
            User.objects.filter(
                username='new-user'
            ).exists()
        )

    def test_user_can_login(self):
        response = self.client.post(
            reverse('users:login'),
            {
                'username': self.user.username,
                'password': 'test-password',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_user_can_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('users:logout')
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_user_can_view_profile(self):
        response = self.client.get(
            reverse(
                'users:profile',
                kwargs={
                    'username': self.user.username,
                },
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['profile'],
            self.user,
        )

    def test_anonymous_user_cannot_edit_profile(self):
        response = self.client.get(
            reverse('users:profile_edit')
        )

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next='
            f'{reverse("users:profile_edit")}',
        )

    def test_authenticated_user_can_edit_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('users:profile_edit'),
            {
                'first_name': 'Updated',
                'last_name': 'User',
                'email': 'updated@example.com',
                'bio': 'Updated biography',
                'date_of_birth': '1999-05-10',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            'Updated',
        )
        self.assertEqual(
            self.user.email,
            'updated@example.com',
        )
        self.assertEqual(
            self.user.date_of_birth.isoformat(),
            '1999-05-10',
        )
