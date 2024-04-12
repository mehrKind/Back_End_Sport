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