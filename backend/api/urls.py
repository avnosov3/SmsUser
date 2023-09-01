from api import views
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', views.CustomUserViewSet, basename='users')
router_v1.register(r'signup', views.SignUpViewSet, 'signup')
router_v1.register(r'login', views.LogInViewSet, 'login')
router_v1.register(r'otp-confirmation', views.OPTConfirmationViewSet, 'otp-confirmation')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
