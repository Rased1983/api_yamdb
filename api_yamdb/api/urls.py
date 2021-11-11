from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, GetTokenView,
                       EmailAndNewUserRegistrationView)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', EmailAndNewUserRegistrationView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
]
