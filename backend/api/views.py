import secrets

from api import serializers, tasks
from django.contrib.auth import authenticate

# from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import OTP, CustomUser

# from backend.settings import ADMIN_EMAIL


class CustomUserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        # if self.request.method in ['POST']:
        #     return serializers.CustomUserCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.CustomUpdateUserSerializer
        return serializers.CustomRetriveListDeleteSerialzer


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user, _ = CustomUser.objects.get_or_create(
                email=email,
            )
            user.set_password(password)
            user.save()
        except IntegrityError:
            return Response(
                'Пользователь с таким password или email уже используется.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(dict(detail='Пользователь успешно создан'), status=status.HTTP_201_CREATED)


class LogInViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LogInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response('Неверный пароль или логин', status=status.HTTP_400_BAD_REQUEST)
        code = str(secrets.randbelow(1000000)).zfill(6)
        otp, _ = OTP.objects.get_or_create(
            user=user,
        )
        otp.code = code
        otp.expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp.save()
        # send_mail(
        #     'Вы зарегистрировались на ресурсе.',
        #     f'Ваш код-подтверждение: {code}',
        #     ADMIN_EMAIL,
        #     (email,),
        #     fail_silently=False,
        # )
        tasks.send_confirmation_code.apply_async(args=[email, code])
        return Response(dict(detail='На электронную почту отправлен код', email=email), status=status.HTTP_200_OK)


class OPTConfirmationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.OPTSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        user = get_object_or_404(CustomUser, email=email)
        otp = get_object_or_404(OTP, user=user)
        if otp.code != code:
            return Response('Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST)
        if otp.expires_at < timezone.now():
            return Response('Время действия кода вышло. Повторите запрос')
        token, _ = Token.objects.get_or_create(user=user)
        return Response(dict(token=str(token.key)), status=status.HTTP_201_CREATED)
