from step import models
from rest_framework import serializers


# class SupportSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.StepSupport
#         fields = "__all__"
        
        
class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = "__all__"