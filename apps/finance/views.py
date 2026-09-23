from rest_framework import viewsets
from .models import ChamaSetting, Expense, Investment
from .serializers import ChamaSettingSerializer, ExpenseSerializer, InvestmentSerializer

class ChamaSettingViewSet(viewsets.ModelViewSet):
    queryset = ChamaSetting.objects.all()
    serializer_class = ChamaSettingSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer