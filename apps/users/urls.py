from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MyProfileView, PolicyViewSet, SignPolicyView

router = DefaultRouter()
router.register(r'policies', PolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', MyProfileView.as_view(), name='profile'),
    path('policies/sign/', SignPolicyView.as_view(), name='sign-policy'),
]