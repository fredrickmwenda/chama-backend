from rest_framework import serializers
from .models import WelfareCase, WelfareContribution

class WelfareContributionSerializer(serializers.ModelSerializer):
    contributor_name = serializers.CharField(source='contributor.name', read_only=True)
    class Meta:
        model = WelfareContribution
        fields = '__all__'

class WelfareCaseSerializer(serializers.ModelSerializer):
    affected_member_name = serializers.CharField(source='affected_member.name', read_only=True)
    contributions = WelfareContributionSerializer(many=True, read_only=True)
    class Meta:
        model = WelfareCase
        fields = '__all__'