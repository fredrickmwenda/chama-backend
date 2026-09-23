from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, record_repayment

router = DefaultRouter()
router.register(r'', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:loan_id>/repay/', record_repayment, name='record-repayment'),
]