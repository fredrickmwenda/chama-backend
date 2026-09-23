from rest_framework import serializers
from .models import Meeting, Contribution, Fine

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class ContributionSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    class Meta:
        model = Contribution
        fields = '__all__'

class FineSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    class Meta:
        model = Fine
        fields = '__all__'