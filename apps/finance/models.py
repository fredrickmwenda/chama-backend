from django.db import models
from django.conf import settings

class ChamaSetting(models.Model):
    financial_year = models.CharField(max_length=20, default="2024-2025")
    financial_year_end = models.DateField(null=True, blank=True) # July 31st
    dividend_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    loan_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=3.0)
    require_collateral = models.BooleanField(default=False)
    # Expense cut percentage (e.g., 5% of savings goes to expenses)
    expense_cut_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.0) 

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Investment(models.Model):
    name = models.CharField(max_length=200)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    expected_return = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


class Transaction(models.Model):
    class Types(models.TextChoices):
        CONTRIBUTION = 'Contribution', 'Contribution'
        LOAN_DISBURSEMENT = 'Loan Disbursement', 'Loan Disbursement'
        LOAN_REPAYMENT = 'Loan Repayment', 'Loan Repayment'
        DIVIDEND = 'Dividend', 'Dividend'
        FINE = 'Fine', 'Fine'
        EXPENSE = 'Expense', 'Expense'

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=30, choices=Types.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, null=True, blank=True) # e.g., Meeting ID or Loan ID
    date = models.DateTimeField(auto_now_add=True)