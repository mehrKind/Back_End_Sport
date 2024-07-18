from rest_framework import serializers
from django.contrib.auth.models import User
from account import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        
class UserProfileSerializer2(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.UserProfile
        fields = ['score', 'profileImage', 'user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = data.pop('user')
        # Add handling for missing fields here if needed
        data.update(user_data)
        return data