from rest_framework import serializers
from django.shortcuts import get_object_or_404

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        model = User


class EmailAndNewUserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email', )
        model = User


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, value):
        user = get_object_or_404(User, username=value['username'])
        if user.confirmation_code != value['confirmation_code']:
            raise serializers.ValidationError(
                "Не правильный токен юзера")
        return value

    class Meta:
        fields = ('username', 'confirmation_code', )
        model = User
