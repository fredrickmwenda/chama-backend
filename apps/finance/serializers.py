from rest_framework import serializers
from .models import ChamaSetting, Expense, Investment

class ChamaSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChamaSetting
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'