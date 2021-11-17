from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (CategoryViewSet, CommentViewSet,
                       email_and_new_user_registration, GenreViewSet,
                       get_token, ReviewViewSet, TitleViewSet, UserViewSet)

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='api_users')
v1_router.register(r'genres', GenreViewSet, basename='api_genres')
v1_router.register(r'categories', CategoryViewSet, basename='api_categories')
v1_router.register(r'titles', TitleViewSet, basename='api_titels')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api_reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api_comments'
)

auth_patterns = [
    path('signup/', email_and_new_user_registration),
    path('token/', get_token),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
