from api import views
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', views.CustomUserViewSet, basename='users')
router_v1.register(r'signup', views.SignUpViewSet, 'signup')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
