import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        'Год выпуска',
        validators=[
        MaxValueValidator(dt.date.today().year)]
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'дата отзыва', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date', ],
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='%(app_label)s_%(class)s_rewiev_unique',
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('текст коммента')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'дата коммента',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
