from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from api.serializers import (
    UserSerializer, EmailAndNewUserRegistrationSerializer, GetTokenSerializer
)
from api.permissions import (
    Admin, AuthorAdminModeratorOrReadOnly, AdminOrReadOnly
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Admin, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete', )

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
                serializer.save()
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
