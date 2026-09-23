# loans/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum
from apps.savings.models import Contribution  # Importing Contribution from the savings app

class Loan(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        DISBURSED = 'Disbursed', 'Disbursed'
        REJECTED = 'Rejected', 'Rejected'

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    collateral_asset = models.CharField(max_length=255, null=True, blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    recommended_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # --- NEW: Amortization & Default Tracking ---
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True) # Next expected payment date

    # Helper Methods for easy calculation in views/serializers
    def total_due(self):
        """ Principal + Total Interest """
        interest = float(self.principal) * (float(self.interest_rate) / 100)
        return float(self.principal) + interest

    def total_paid(self):
        """ Sum of all repayments made """
        return float(self.repayments.aggregate(Sum('amount'))['amount__sum'] or 0)

    def balance(self):
        """ Remaining amount to clear the loan """
        return self.total_due() - self.total_paid()

    def __str__(self):
        return f"Loan #{self.id} - {self.member.username} ({self.status})"


class LoanGuarantor(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='guarantors')
    guarantor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_guaranteed = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True) # Becomes False if loan is fully paid

    def clean(self):
        """ Validate that the guarantor has enough savings BEFORE saving to DB """
        super().clean()
        
        # Calculate guarantor's total savings
        guarantor_savings = Contribution.objects.filter(member=self.guarantor).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        
        # (Optional advanced logic): You could also subtract amounts they are already guaranteeing for other loans here.
        
        if self.amount_guaranteed > float(guarantor_savings):
            raise ValidationError(
                f"{self.guarantor.username} does not have enough savings to guarantee KES {self.amount_guaranteed}. "
                f"Available savings: KES {guarantor_savings}"
            )

    def save(self, *args, **kwargs):
        # Run validation checks before actually saving the object
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guarantor.username} guarantees KES {self.amount_guaranteed} for Loan #{self.loan.id}"


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repayment of KES {self.amount} for Loan #{self.loan.id}"


# --- NEW: Automated Default Fines ---
class LoanDefaultFine(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='default_fines')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine of KES {self.amount} on Loan #{self.loan.id} ({'Paid' if self.is_paid else 'Unpaid'})"