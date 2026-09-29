# apps/loans/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum
from apps.savings.models import Contribution

class Loan(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        DISBURSED = 'Disbursed', 'Disbursed'
        REJECTED = 'Rejected', 'Rejected'

    class Frequency(models.TextChoices):
        ONE_TIME = 'One Time', 'One Time'
        WEEKLY = 'Weekly', 'Weekly'
        BI_WEEKLY = 'Bi-Weekly', 'Bi-Weekly'
        MONTHLY = 'Monthly', 'Monthly'

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    date_applied = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)


    # --- NEW: Repayment Frequency ---
    repayment_frequency = models.CharField(max_length=20, choices=Frequency.choices, default=Frequency.MONTHLY)
    
    # Amortization & Default Tracking
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)

    # --- NEW: Digital Signatures (Stored as Base64 Text) ---
    chairperson_signature = models.TextField(null=True, blank=True)
    secretary_signature = models.TextField(null=True, blank=True)
    treasurer_signature = models.TextField(null=True, blank=True)

    def total_due(self):
        interest = float(self.principal) * (float(self.interest_rate) / 100)
        return float(self.principal) + interest

    def total_paid(self):
        return float(self.repayments.aggregate(Sum('amount'))['amount__sum'] or 0)

    def balance(self):
        return self.total_due() - self.total_paid()

    def __str__(self):
        return f"Loan #{self.id} - {self.member.username} ({self.status})"


class LoanSecurity(models.Model):
    class Condition(models.TextChoices):
        EXCELLENT = 'Excellent', 'Excellent'
        GOOD = 'Good', 'Good'
        FAIR = 'Fair', 'Fair'
        POOR = 'Poor', 'Poor'

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='securities')
    item_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)

    def __str__(self):
        return f"{self.item_name} (KES {self.estimated_value})"


class LoanGuarantor(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='guarantors')
    guarantor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_guaranteed = models.DecimalField(max_digits=10, decimal_places=2)
    date_signed = models.DateTimeField(auto_now_add=True)
    is_signed = models.BooleanField(default=True) # Acts as digital signature

    def clean(self):
        super().clean()
        guarantor_savings = Contribution.objects.filter(member=self.guarantor).aggregate(Sum('amount'))['amount__sum'] or 0
        if self.amount_guaranteed > float(guarantor_savings):
            raise ValidationError(f"{self.guarantor.username} does not have enough savings to guarantee KES {self.amount_guaranteed}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guarantor.username} guarantees KES {self.amount_guaranteed} for Loan #{self.loan.id}"

class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class LoanDefaultFine(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='default_fines')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)