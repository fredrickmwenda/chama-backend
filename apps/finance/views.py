from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import ChamaSetting, Expense, Investment
from .serializers import ChamaSettingSerializer, ExpenseSerializer, InvestmentSerializer

class ChamaSettingView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChamaSettingSerializer

    def get_object(self):
        # Ensures there is always exactly one settings object (Singleton pattern)
        setting, created = ChamaSetting.objects.get_or_create(id=1)
        return setting

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer