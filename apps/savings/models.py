from django.db import models
from django.conf import settings

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    meeting_type = models.CharField(max_length=10, default='Money')
    minimum_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_complete = models.BooleanField(default=False)

class Contribution(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Fine(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00) # Default fine
    reason = models.CharField(max_length=255, default="Absenteeism")
    is_paid = models.BooleanField(default=False)