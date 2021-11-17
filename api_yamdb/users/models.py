from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import username_validator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USER_ROLES = ((USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Никнейм',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
    )
    role = models.TextField(
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='Код подтверждения',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_admin
