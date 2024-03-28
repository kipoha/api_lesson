from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import User

class UserCreateValidate(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise exceptions.ValidationError('user already exists!')

class UserLoginValidate(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserConfirmValidate(serializers.Serializer):
    code = serializers.IntegerField()