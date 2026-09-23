from django.db import models
from django.conf import settings

class WelfareCase(models.Model):
    CASE_TYPES = [('Death', 'Death'), ('Sickness', 'Sickness'), ('Emergency', 'Emergency')]
    affected_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    # ADD THIS FIELD:
    date_created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.case_type} - {self.affected_member.username}"

class WelfareContribution(models.Model):
    welfare_case = models.ForeignKey(WelfareCase, on_delete=models.CASCADE)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)