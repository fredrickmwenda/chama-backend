from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.db import transaction
from apps.finance.models import ChamaSetting
from apps.savings.models import Contribution
from .models import Loan, Repayment
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('-date_applied')
    serializer_class = LoanSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        member_id = request.data.get('member')
        amount_requested = float(request.data.get('principal', 0))
        
        try:
            # Check active loans (Rule: No new loan if active loan exists)
            active_loans = Loan.objects.filter(member_id=member_id, is_paid=False)
            if active_loans.exists():
                return Response({"error": "Loan denied. Member has an active loan."}, status=status.HTTP_400_BAD_REQUEST)

            # Check Savings Multiplier
            settings = ChamaSetting.objects.first()
            multiplier = float(settings.loan_multiplier) if settings else 3.0
            total_savings = Contribution.objects.filter(member_id=member_id).aggregate(Sum('amount'))['amount__sum'] or 0
            max_limit = float(total_savings) * multiplier

            if amount_requested > max_limit:
                return Response({"error": f"Loan denied. Max limit is KES {max_limit:,.2f}."}, status=status.HTTP_400_BAD_REQUEST)

            # Check Collateral
            if settings and settings.require_collateral:
                if not request.data.get('collateral_asset'):
                    return Response({"error": "Loan denied. Collateral (Logbook) is required."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

@transaction.atomic
@api_view(['POST'])
def record_repayment(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

    if loan.is_paid:
        return Response({"error": "Loan already fully paid."}, status=status.HTTP_400_BAD_REQUEST)

    amount = float(request.data.get('amount', 0))
    if amount <= 0:
        return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

    principal = float(loan.principal)
    interest = principal * (float(loan.interest_rate) / 100)
    total_due = principal + interest

    total_paid = float(loan.repayments.aggregate(Sum('amount'))['amount__sum'] or 0)
    remaining = total_due - total_paid

    if amount > remaining:
        return Response({"error": f"Overpayment. Remaining balance is KES {remaining:,.2f}."}, status=status.HTTP_400_BAD_REQUEST)

    repayment = Repayment.objects.create(loan=loan, amount=amount)
    new_total_paid = total_paid + amount

    if new_total_paid >= total_due:
        loan.is_paid = True
        loan.save()

    return Response({
        "message": "Repayment successful." if not loan.is_paid else "Loan fully paid and closed!",
        "remaining_balance": total_due - new_total_paid
    }, status=status.HTTP_201_CREATED)