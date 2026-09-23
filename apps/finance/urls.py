from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChamaSettingViewSet, ExpenseViewSet, InvestmentViewSet

router = DefaultRouter()
router.register(r'settings', ChamaSettingViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'investments', InvestmentViewSet)

urlpatterns = [path('', include(router.urls))]