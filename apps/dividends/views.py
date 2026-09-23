from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from apps.finance.models import ChamaSetting
from apps.savings.models import Contribution
from apps.users.models import Member
from .models import Dividend
from .serializers import DividendSerializer

class DividendViewSet(viewsets.ModelViewSet):
    queryset = Dividend.objects.all().order_by('-date_disbursed')
    serializer_class = DividendSerializer

@api_view(['POST'])
def announce_dividends(request):
    settings = ChamaSetting.objects.first()
    if not settings:
        return Response({"error": "Settings not configured"}, status=400)
    
    percentage = float(request.data.get('percentage', settings.dividend_percentage))
    financial_year = request.data.get('financial_year', settings.financial_year)
    
    settings.dividend_percentage = percentage
    settings.financial_year = financial_year
    settings.is_announced = True
    settings.announcement_date = timezone.now()
    settings.disbursement_date = timezone.now() + timedelta(days=7)
    settings.save()

    Dividend.objects.filter(financial_year=financial_year, is_disbursed=False).delete()

    members = Member.objects.all()
    for member in members:
        total_saved = Contribution.objects.filter(member=member).aggregate(Sum('amount'))['amount__sum'] or 0
        dividend_amount = (float(total_saved) * percentage) / 100
        
        if dividend_amount > 0:
            Dividend.objects.create(
                member=member, financial_year=financial_year, amount=dividend_amount,
                is_reinvested=(member.dividend_preference == 'Reinvest')
            )
    
    return Response({"message": "Dividends announced successfully."})

@transaction.atomic
@api_view(['POST'])
def disburse_dividends(request):
    settings = ChamaSetting.objects.first()
    if not settings or not settings.can_disburse:
        return Response({"error": "7-day waiting period active."}, status=403)

    pending = Dividend.objects.filter(is_disbursed=False, financial_year=settings.financial_year)
    
    for div in pending:
        if div.is_reinvested:
            Contribution.objects.create(member=div.member, amount=div.amount)
        div.is_disbursed = True
        div.date_disbursed = timezone.now()
        div.save()

    return Response({"message": f"Successfully disbursed {pending.count()} dividends."})