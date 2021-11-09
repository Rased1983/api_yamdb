from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
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
