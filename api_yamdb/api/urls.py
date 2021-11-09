from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')

urlpatterns = [
    path('v1/', include(router.urls)),
]
