from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from users import settings


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Юзернейм',
        unique=True,
        blank=True,
        max_length=settings.MAIN_LENGTH
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        max_length=settings.MAIN_LENGTH
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAIN_LENGTH
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAIN_LENGTH
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.CharField(
        blank=True,
        verbose_name='Код подтверждения',
        max_length=settings.CODE_LENGTH
    )
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=2))
