from step.models import StepSupport
from rest_framework import serializers


class SupportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StepSupport
        fields = "__all__"