from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WelfareCaseViewSet, WelfareContributionViewSet

router = DefaultRouter()
router.register(r'cases', WelfareCaseViewSet)
router.register(r'contributions', WelfareContributionViewSet)

urlpatterns = [path('', include(router.urls))]