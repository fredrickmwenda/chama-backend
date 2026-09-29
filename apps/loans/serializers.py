# apps/loans/serializers.py
from rest_framework import serializers
from .models import Loan, Repayment, LoanSecurity, LoanGuarantor

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'

class LoanSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSecurity
        fields = '__all__'

class LoanGuarantorSerializer(serializers.ModelSerializer):
    guarantor_name = serializers.CharField(source='guarantor.username', read_only=True)
    class Meta:
        model = LoanGuarantor
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.username', read_only=True)
    repayments = RepaymentSerializer(many=True, read_only=True)
    securities = LoanSecuritySerializer(many=True, read_only=True)
    guarantors = LoanGuarantorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Loan
        fields = '__all__'