from django.db import models
from django.conf import settings

class Dividend(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    financial_year = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_disbursed = models.BooleanField(default=False)
    is_reinvested = models.BooleanField(default=False)
    date_disbursed = models.DateTimeField(null=True, blank=True)