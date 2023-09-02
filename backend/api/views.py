import secrets

from api import constants, serializers, tasks
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from djoser.serializers import SetPasswordSerializer
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import OTP, CustomUser


class CustomUserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.CustomUpdateUserSerializer
        return serializers.CustomRetriveListDeleteSerialzer


class ChangePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SetPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.EmailPasswordSerializer

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
                constants.USER_EXISTS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(dict(detail=constants.USER_CREATED), status=status.HTTP_201_CREATED)


class LogInViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.EmailPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response(constants.WRONG_PASSWORD_OR_LOGIN, status=status.HTTP_400_BAD_REQUEST)
        code = str(secrets.randbelow(1000000)).zfill(6)
        otp, _ = OTP.objects.get_or_create(
            user=user,
        )
        otp.code = code
        otp.expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp.save()
        tasks.send_confirmation_code.apply_async(args=[email, code])
        return Response(dict(detail=constants.CODE_SENT_TO_MAIL, email=email), status=status.HTTP_200_OK)


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
            return Response(constants.WRONG_CODE, status=status.HTTP_400_BAD_REQUEST)
        if otp.expires_at < timezone.now():
            return Response(constants.TIME_EXPIRED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(dict(token=str(token.key)), status=status.HTTP_201_CREATED)
