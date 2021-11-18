from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class EmailAndNewUserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Имя "me" зарезирвировано для системных нужд')
        return value

    def validate(self, value):
        username = value['username']
        email = value['email']
        user1_isexists = User.objects.filter(username=username).exists()
        user2_isexists = User.objects.filter(email=email).exists()
        if user1_isexists and user2_isexists:
            user1 = User.objects.get(username=username)
            user2 = User.objects.get(email=email)
            if user1 != user2:
                raise ValidationError('Имя или почта указаны неверно!')
            return value
        if user1_isexists or user2_isexists:
            raise ValidationError('Имя или почта уже заняты!')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, value):
        user = get_object_or_404(User, username=value['username'])
        token = value['confirmation_code']
        if not default_token_generator.check_token(user, token):
            raise ValidationError('Неправильный токен юзера')
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CustomSlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {"name": value.name, 'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    genre = CustomSlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = CustomSlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, value):
        if self.context['request'].method != 'POST':
            return value
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id'))
        if Review.objects.filter(author=self.context['request'].user,
                                 title=title).exists():
            raise ValidationError('Нельзя оставить повторный отзыв!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
