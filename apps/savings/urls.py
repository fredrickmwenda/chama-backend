from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet, ContributionViewSet, FineViewSet

router = DefaultRouter()
router.register(r'meetings', MeetingViewSet)
router.register(r'contributions', ContributionViewSet)
router.register(r'fines', FineViewSet)

urlpatterns = [path('', include(router.urls))]