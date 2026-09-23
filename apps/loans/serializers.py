from rest_framework import serializers
from .models import Loan, Repayment

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    repayments = RepaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'