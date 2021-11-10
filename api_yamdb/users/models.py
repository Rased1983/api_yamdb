from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    
    def username_validator(self):
        if self.username == 'me':
            raise ValidationError('Имя "me" зарезирвировано для системных нужд')
    
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    role = models.TextField(
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR or self.is_admin
