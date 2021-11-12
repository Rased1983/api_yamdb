from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Review, Title
from users.models import User
from users.utils import random_code_for_user
from reviews.models import Genre, Category
from api.serializers import (
    UserSerializer, EmailAndNewUserRegistrationSerializer, GetTokenSerializer, GenreSerializer, CategorySerializer
)
from api.permissions import (
    Admin, AuthorAdminModeratorOrReadOnly, AdminOrReadOnly
)
from .serializers import (CategorySerializer,CommentSerializer,
                          GenreSerializer, ReadTitleSerializer,
                          ReviewSerializer, WriteTitleSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Admin, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        serializer.save(confirmation_code=random_code_for_user())

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'GET':
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailAndNewUserRegistrationView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = EmailAndNewUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if not User.objects.filter(username=username).exists():
                serializer.save(confirmation_code=random_code_for_user())
            user = get_object_or_404(User, username=username)
            send_mail(
                subject='Request of token',
                message=(f'Приятного времени суток!\n'
                         f'username: {username}\n'
                         f'confirmation_code: {user.confirmation_code}'),
                from_email='yamdb@mail.com',
                recipient_list=(email,),
            )
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            return Response(
                {
                    'token': str(AccessToken.for_user(user))
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', )
    lookup_field = 'slug'
    http_method_names = ('get', 'post', 'delete')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', )
    lookup_field = 'slug'
    http_method_names = ('get', 'post', 'delete')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return WriteTitleSerializer
        return ReadTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(
            Review, title=title, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(review=review, author=self.request.user)
