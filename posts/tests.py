from django.test import TestCase

from .forms import PostForm


class PostFormTest(TestCase):
    def test_valid_form(self):
        form = PostForm(
            data={
                'topic': 'Тестовый пост',
                'content': 'Это корректный текст.',
            }
        )

        self.assertTrue(form.is_valid())

    def test_empty_content(self):
        form = PostForm(
            data={
                'topic': 'Тестовый пост',
                'content': '',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_content_too_short(self):
        form = PostForm(
            data={
                'topic': 'Тестовый пост',
                'content': '123456789',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_image_is_optional(self):
        form = PostForm(
            data={
                'topic': 'Тестовый пост',
                'content': 'Это корректный текст.',
            }
        )

        self.assertTrue(form.is_valid())

    def test_author_is_not_form_field(self):
        self.assertNotIn('author', PostForm().fields)
