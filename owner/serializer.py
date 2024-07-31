from rest_framework import serializers
from owner import models

class DailyInfoSerializer(serializers.ModelSerializer):
    totalStep = serializers.SerializerMethodField()

    class Meta:
        model = models.DailyInfo
        fields = "__all__"  # This will include all fields from the model

    def get_totalStep(self, obj):
        return obj.totalStep  # Access the totalStep property of the DailyInfo instance
