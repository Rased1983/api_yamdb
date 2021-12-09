import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(dt.date.today().year)],
        verbose_name='Год выпуска',
        db_index=True,
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Оглавление',
    )
    text = models.TextField(verbose_name='Текст', )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        verbose_name='оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='rewiev_unique_name',
            )
        ]

    def __str__(self):
        return f'Отзыв к фильму: "{self.title}", автор: {self.author}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='текст комментария', )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата комментария',
    )

    class Meta:
        ordering = ['-pub_date']
