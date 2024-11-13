from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'fullname', 'gender', 'birthday','telephone','role']


class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=15)
    fullname = serializers.CharField(max_length=255)
    birthday = serializers.DateField()
    gender = serializers.BooleanField()
    role = serializers.ChoiceField(choices=ERole.choices, required=False)


class AuthenticationRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'fullname', 'role']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        if hasattr(user, 'role'):  # Nếu có trường role
            token['role'] = user.role

        return token

