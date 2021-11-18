from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import SpecialTitlesFilter
from api.permissions import (Admin, AdminOrReadOnly,
                             AuthorAdminModeratorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             EmailAndNewUserRegistrationSerializer,
                             GenreSerializer, GetTokenSerializer,
                             ReviewSerializer, UserSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User
from users.utils import send_confirmation_code


class SpecialCastomMixin(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Admin, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_and_new_user_registration(request):
    serializer = EmailAndNewUserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = User.objects.get_or_create(username=username, email=email)
    user = user[0]
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_confirmation_code(user)
    return Response(serializer.validated_data,
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    return Response({'token': str(AccessToken.for_user(user))},
                    status=status.HTTP_200_OK)


class GenreViewSet(SpecialCastomMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(SpecialCastomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SpecialTitlesFilter
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   title__id=self.kwargs['title_id'],
                                   id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   title__id=self.kwargs['title_id'],
                                   id=self.kwargs['review_id'])
        serializer.save(review=review, author=self.request.user)
