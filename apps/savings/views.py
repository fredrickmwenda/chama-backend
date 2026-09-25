from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Meeting, Contribution, Fine
from .serializers import MeetingSerializer, ContributionSerializer, FineSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all().order_by('-date')
    serializer_class = MeetingSerializer

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all().order_by('-date')
    serializer_class = ContributionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['meeting'] # Allows: /savings/contributions/?meeting=1

    def create(self, request, *args, **kwargs):
        meeting_id = request.data.get('meeting')
        amount = float(request.data.get('amount', 0))
        
        if meeting_id:
            meeting = Meeting.objects.get(id=meeting_id)
            if meeting.meeting_type == 'Money' and amount < float(meeting.minimum_contribution):
                return Response(
                    {"error": f"Contribution must be at least KES {meeting.minimum_contribution} for this meeting."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().create(request, *args, **kwargs)

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all().order_by('-is_paid', '-meeting__date')
    serializer_class = FineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['meeting'] # Allows: /savings/fines/?meeting=1