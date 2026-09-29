# apps/finance/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChamaSettingView, ExpenseViewSet, InvestmentViewSet

router = DefaultRouter()
# Routers are for ViewSets (like Expenses and Investments)
router.register(r'expenses', ExpenseViewSet)
router.register(r'investments', InvestmentViewSet)

urlpatterns = [
    # Explicit path for the Singleton Settings View
    path('settings/', ChamaSettingView.as_view(), name='chama-settings'),
    
    # Include the router URLs for expenses and investments
    path('', include(router.urls)),
]