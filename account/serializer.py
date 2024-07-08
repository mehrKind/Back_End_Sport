from rest_framework import serializers
from django.contrib.auth.models import User
from account import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "is_active", "last_login", "date_joined")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        
class UserProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['score']  # Add other fields you want to include here

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add handling for missing fields here if needed
        return data
