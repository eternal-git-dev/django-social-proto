from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from users.validators import validate_image_size

TOPIC_MAX_LENGTH = 128
CONTENT_MIN_LENGTH = 10


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    topic = models.CharField(
        verbose_name='Заголовок',
        max_length=TOPIC_MAX_LENGTH
    )
    content = models.TextField(
        verbose_name='Текст',
        validators=[MinLengthValidator(CONTENT_MIN_LENGTH)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        verbose_name='Фото поста',
        upload_to='posts/',
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("-created_at",)

    def __str__(self):
        return f'Пост {self.topic}'
