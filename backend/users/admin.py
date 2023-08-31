from django.contrib import admin

from users import models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    empty_value_display = '-пусто-'


@admin.register(models.OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
