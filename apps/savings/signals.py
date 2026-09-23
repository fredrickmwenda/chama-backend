# savings/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Contribution
from apps.finance.models import ChamaSetting, Expense, Transaction

@receiver(post_save, sender=Contribution)
def deduct_expense_cut(sender, instance, created, **kwargs):
    if created:
        settings = ChamaSetting.objects.first()
        if settings and settings.expense_cut_percentage > 0:
            # Calculate the cut amount
            cut_amount = (float(instance.amount) * float(settings.expense_cut_percentage)) / 100
            
            # Use database transaction to ensure both records are created safely
            with transaction.atomic():
                # 1. Record the expense cut
                Expense.objects.create(
                    description=f"Expense cut for {instance.member.username}'s contribution",
                    amount=cut_amount
                )
                
                # 2. Log this in the Unified Transaction Ledger
                Transaction.objects.create(
                    member=instance.member,
                    transaction_type=Transaction.Types.EXPENSE,
                    amount=cut_amount,
                    reference=f"Expense cut for Contribution #{instance.id}"
                )