from django.db import models
from django.conf import settings

# apps/finance/models.py
from django.db import models

class ChamaSetting(models.Model):
    # --- General Chama Info ---
    chama_name = models.CharField(max_length=200, default="My Chama")
    logo = models.ImageField(upload_to='chama_logos/', null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # --- Financial Rules & Fines ---
    financial_year = models.CharField(max_length=20, default="2024-2025")
    dividend_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    loan_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=3.0)
    require_collateral = models.BooleanField(default=False)
    expense_cut_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    
    late_fine = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    absentee_fine = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)
    non_payment_fine = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    # --- Notification Channels ---
    class SmsProviders(models.TextChoices):
        AFRICAS_TALKING = 'Africas Talking', 'Africas Talking'
        TWILIO = 'Twilio', 'Twilio'

    notify_sms = models.BooleanField(default=False)
    sms_provider = models.CharField(max_length=50, choices=SmsProviders.choices, null=True, blank=True)
    sms_api_key = models.CharField(max_length=255, null=True, blank=True)
    sms_sender_id = models.CharField(max_length=50, null=True, blank=True)

    notify_email = models.BooleanField(default=True)
    email_host = models.CharField(max_length=255, null=True, blank=True, help_text="e.g., smtp.gmail.com")
    email_host_user = models.CharField(max_length=255, null=True, blank=True)
    email_host_password = models.CharField(max_length=255, null=True, blank=True)

    notify_whatsapp = models.BooleanField(default=False)
    whatsapp_api_key = models.CharField(max_length=255, null=True, blank=True, help_text="Meta Cloud API Key")
    whatsapp_phone_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.chama_name

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