from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WelfareCase, WelfareContribution

@receiver(post_save, sender=WelfareContribution)
def update_welfare_amount_raised(sender, instance, created, **kwargs):
    if created:
        welfare_case = instance.welfare_case
        # Recalculate total raised
        total_raised = WelfareContribution.objects.filter(welfare_case=welfare_case).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        welfare_case.amount_raised = total_raised
        
        # Auto-close case if target is met
        if total_raised >= welfare_case.target_amount:
            welfare_case.is_active = False
            
        welfare_case.save()