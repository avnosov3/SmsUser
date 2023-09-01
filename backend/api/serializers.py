from rest_framework import serializers

from users import settings as users_settings
from users.models import CustomUser


class CustomUpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
        )


class CustomRetriveListDeleteSerialzer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=users_settings.MAIN_LENGTH)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)


class LogInSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=True,
        max_length=users_settings.MAIN_LENGTH,
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=users_settings.CODE_LENGTH,
    )
