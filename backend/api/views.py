import secrets

from api import serializers
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from backend.settings import ADMIN_EMAIL

from users.models import OTP, CustomUser


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
    serializer_class = serializers.SignupSerializer

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
                'Проблема в аутентификации: Пользователь с таким password или email уже используется.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        code = str(secrets.randbelow(1000000)).zfill(6)
        user.save()
        otp, _ = OTP.objects.get_or_create(
            user=user,
        )
        otp.code = code
        otp.expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp.save()
        send_mail(
            'Вы зарегистрировались на ресурсе.',
            f'Ваш код-подтверждение: {code}',
            ADMIN_EMAIL,
            (email,),
            fail_silently=False,
        )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
