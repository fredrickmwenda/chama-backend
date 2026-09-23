from rest_framework import viewsets
from .models import WelfareCase, WelfareContribution
from .serializers import WelfareCaseSerializer, WelfareContributionSerializer

class WelfareCaseViewSet(viewsets.ModelViewSet):
    queryset = WelfareCase.objects.all().order_by('-is_active', '-date_created')
    serializer_class = WelfareCaseSerializer

class WelfareContributionViewSet(viewsets.ModelViewSet):
    queryset = WelfareContribution.objects.all().order_by('-date')
    serializer_class = WelfareContributionSerializer