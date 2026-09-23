from rest_framework import serializers
from .models import Dividend

class DividendSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    class Meta:
        model = Dividend
        fields = '__all__'