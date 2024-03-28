from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from users import models
from django.core.mail import send_mail
from shop_api import settings
import datetime 
from django.utils import timezone

@api_view(['POST'])
def reg_user_api_view(request):
    serializer = serializers.UserCreateValidate(data=request.data)

    serializer.is_valid(raise_exception=True)
    
    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        email=serializer.validated_data['email'],
        is_active=False
        )
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expiry_date = timezone.now() + datetime.timedelta(minutes=10)
    user_code = models.Code.objects.create(user=user, code=code, expiry_date=expiry_date)
    send_mail('Verify', f'your code: {code}\n code expiration date: 10 min', settings.EMAIL_HOST_USER, recipient_list=[user.email])
    
    return Response(data={'user_id': user.id, 'code': user_code.code, 'code expiration date': '10min'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def auth_user_api_view(request):
    serializer = serializers.UserLoginValidate(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key})
    return Response(data={'error': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = serializers.UserConfirmValidate(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    code_user = models.Code.objects.filter(code=serializer.validated_data['code']).first()
    if not code_user:
        return Response(data={'code': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    expiry_date = timezone.now() + datetime.timedelta(minutes=10)
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    if code_user.expiry_date < timezone.now():
        code_user.delete()
        user_code = models.Code.objects.create(user=code_user.user, code=code, expiry_date=expiry_date)
        send_mail('Verify', f'your code: {code}\n code expiration date: 10min', settings.EMAIL_HOST_USER, recipient_list=[code_user.user.email])
        return Response(data={'error': 'code expired', 'new code': user_code.code, 'code expiration date': '10min'}, status=status.HTTP_400_BAD_REQUEST)
    
    code_user.user.is_active = True
    code_user.user.save()
    code_user.delete()
    return Response(data={'status': 'your account is active!'}, status=status.HTTP_200_OK)