from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DividendViewSet, announce_dividends, disburse_dividends

router = DefaultRouter()
router.register(r'', DividendViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('announce/', announce_dividends, name='announce-dividends'),
    path('disburse/', disburse_dividends, name='disburse-dividends'),
]