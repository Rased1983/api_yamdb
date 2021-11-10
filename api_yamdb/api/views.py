from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination

from users.models import User
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
