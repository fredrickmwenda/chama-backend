from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=50, default='Member')
    dividend_preference = models.CharField(max_length=10, default='Cash')
    # Performance tracking can be done dynamically via queries, no field needed here

class Policy(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    version = models.FloatField(default=1.0)

class UserPolicySignature(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=True)