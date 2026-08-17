from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from users.validators import validate_image_size, validate_date_of_birth


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        verbose_name='Фото',
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image_size]
    )
    bio = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
        validators=[validate_date_of_birth]
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        validators=[EmailValidator]
    )


    def __str__(self):
        return f'Аккаунт пользователя {self.username}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
