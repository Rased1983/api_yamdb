from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):

    def username_validator(username):
        if username == 'me':
            raise ValidationError(
                'Имя "me" зарезирвировано для системных нужд'
            )

    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )

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
        max_length=10,
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Код подтверждения',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def is_who(self):
        if self.is_superuser or self.role == 'admin':
            return 'admin'
        elif self.role == 'moderator':
            return 'moderator'
        else:
            return 'user'
