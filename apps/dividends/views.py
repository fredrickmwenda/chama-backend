from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from datetime import timedelta
from apps.finance.models import ChamaSetting
from apps.savings.models import Contribution
from apps.users.models import Member
from .models import Dividend
from .serializers import DividendSerializer

class DividendViewSet(viewsets.ModelViewSet):
    queryset = Dividend.objects.all().order_by('-date_disbursed')
    serializer_class = DividendSerializer

@api_view(['GET'])
def calculate_dividends(request):
    settings = ChamaSetting.objects.first()
    if not settings:
        return Response({"error": "Settings not configured"}, status=400)
    
    rule = request.query_params.get('rule', 'YEARLY')
    percentage = float(settings.dividend_percentage)
    
    # Calculate Total Group Savings based on rule
    if rule == 'CUTOFF':
        cutoff_date = timezone.now().replace(month=7, day=1)
        group_contributions = Contribution.objects.filter(date__lte=cutoff_date).aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        group_contributions = Contribution.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    total_pool = float(group_contributions) * (percentage / 100)
    members = Member.objects.all()
    distribution = []

    for member in members:
        if rule == 'CUTOFF':
            cutoff_date = timezone.now().replace(month=7, day=1)
            member_contrib = Contribution.objects.filter(member=member.user, date__lte=cutoff_date).aggregate(Sum('amount'))['amount__sum'] or 0
            total_contrib = Contribution.objects.filter(member=member.user).aggregate(Sum('amount'))['amount__sum'] or 0
        else:
            member_contrib = Contribution.objects.filter(member=member.user).aggregate(Sum('amount'))['amount__sum'] or 0
            total_contrib = member_contrib

        # Calculate share safely (prevent division by zero)
        share = (float(member_contrib) / float(group_contributions)) * 100 if group_contributions > 0 else 0
        dividend_amount = (share / 100) * total_pool
        
        # Check if already disbursed
        existing = Dividend.objects.filter(member=member.user, financial_year=settings.financial_year).first()
        status_str = "Approved" if existing and existing.is_disbursed else "Pending"
        
        distribution.append({
            "id": member.id,
            "name": member.name,
            "total_contribution": float(total_contrib),
            "qualifying_contribution": float(member_contrib),
            "share": round(share, 2),
            "dividend": round(dividend_amount, 2),
            "status": status_str
        })

    return Response({
        "total_pool": round(total_pool, 2),
        "approved_total": sum(d['dividend'] for d in distribution if d['status'] == 'Approved'),
        "pending_approval": sum(d['dividend'] for d in distribution if d['status'] == 'Pending'),
        "paid_out": 0,
        "distribution": distribution
    })

@api_view(['POST'])
def announce_dividends(request):
    settings = ChamaSetting.objects.first()
    if not settings:
        return Response({"error": "Settings not configured"}, status=400)
    
    settings.is_announced = True
    settings.announcement_date = timezone.now()
    settings.disbursement_date = timezone.now() + timedelta(days=7)
    settings.save()

    # Create Pending Dividend records for all members
    members = Member.objects.all()
    for member in members:
        Dividend.objects.get_or_create(
            member=member.user, financial_year=settings.financial_year,
            defaults={'amount': 0, 'is_disbursed': False}
        )

    return Response({"message": "Dividends announced successfully. Members can now view their pending payouts."})

@transaction.atomic
@api_view(['POST'])
def disburse_dividends(request):
    member_ids = request.data.get('member_ids', [])
    if not member_ids:
        return Response({"error": "No members selected."}, status=400)

    settings = ChamaSetting.objects.first()
    if not settings:
        return Response({"error": "Settings not configured"}, status=400)

    rule = request.data.get('rule', 'YEARLY')
    calc_response = calculate_dividends(request)
    calc_data = calc_response.data.get('distribution', [])

    disbursed_count = 0
    for item in calc_data:
        if item['id'] in member_ids and item['status'] == 'Pending':
            member = Member.objects.get(id=item['id'])
            div, created = Dividend.objects.update_or_create(
                member=member.user, financial_year=settings.financial_year,
                defaults={'amount': item['dividend'], 'is_disbursed': True, 'date_disbursed': timezone.now()}
            )
            
            if member.dividend_preference == 'Reinvest':
                Contribution.objects.create(member=member.user, amount=item['dividend'])
            
            disbursed_count += 1

    return Response({"message": f"Successfully disbursed dividends to {disbursed_count} members."})