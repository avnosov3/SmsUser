from django.urls import include, path
from rest_framework import routers

from api import views

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', views.CustomUserViewSet, basename='users')
router_v1.register(r'signup', views.SignUpViewSet, 'signup')
router_v1.register(r'login', views.LogInViewSet, 'login')
router_v1.register(r'otp-confirmation', views.OPTConfirmationViewSet, 'otp-confirmation')
router_v1.register(r'change-password', views.ChangePasswordViewSet, basename='change-password')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
