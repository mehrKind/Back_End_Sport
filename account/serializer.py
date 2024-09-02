from rest_framework import serializers
from django.contrib.auth.models import User
from account import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name")
        
        
class UserSerializer_email(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)  # Assuming you want to make email optional too

    class Meta:
        model = User
        fields = ("username", "first_name", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        
class UserProfileSerializer2(serializers.ModelSerializer):
    user = UserSerializer_email()

    class Meta:
        model = models.UserProfile
        fields = ['score', 'profileImage', 'user', "level", "weight", "height", "city", "provinces"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = data.pop('user')
        # Flatten the user data into the main dictionary
        data.update(user_data)
        return data

    def update(self, instance, validated_data):
        profile_image = serializers.ImageField(required=False)
        # Extract user data from the validated data
        user_data = validated_data.pop('user', None)

        # Update User model fields
        if user_data:
            user = instance.user
            if 'username' in user_data:
                user.username = user_data['username']
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'email' in user_data:
                user.email = user_data['email']
            user.save()

        # Update UserProfile model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
