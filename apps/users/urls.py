from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, CustomLoginView, MyProfileView, PolicyViewSet, SignPolicyView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'policies', PolicyViewSet, basename='policy')

urlpatterns = [
    # Router URLs (Members & Policies)
    path('', include(router.urls)),
    
    # Auth routes
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', MyProfileView.as_view(), name='profile'),
    path('auth/policies/sign/', SignPolicyView.as_view(), name='sign-policy'),
]