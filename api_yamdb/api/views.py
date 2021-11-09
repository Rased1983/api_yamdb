from rest_framework import status, viewsets

from users.models import User
from api.serializers import UserSerializer
from api.pagination import CustomPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()
    pagination_class = CustomPagination
    lookup_field = 'username'