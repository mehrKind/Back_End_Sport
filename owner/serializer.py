from rest_framework import serializers
from owner import models

class DailyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyInfo
        fields = "__all__"
