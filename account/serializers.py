
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from xml.dom import ValidationErr
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'Fname', 'Lname', 'password', 'password2']  
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError("Password and confirm password do not match")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email', 'password']  
      

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','Fname','Lname','id','is_admin']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length = 255, style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')


        if password != password2:
            raise serializers.ValidationError("Password and confirm password do not match")
        user.set_password(password)
        user.save()
        return attrs


