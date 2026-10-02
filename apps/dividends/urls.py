# apps/dividends/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DividendViewSet, announce_dividends, disburse_dividends, calculate_dividends

router = DefaultRouter()
router.register(r'', DividendViewSet)

urlpatterns = [
    # 1. Custom routes MUST go FIRST so Django finds them before assuming "calculate" is an ID
    path('calculate/', calculate_dividends, name='calculate-dividends'),
    path('announce/', announce_dividends, name='announce-dividends'),
    path('disburse/', disburse_dividends, name='disburse-dividends'),
    
    # 2. Router goes LAST
    path('', include(router.urls)),
]