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
    profileImage = serializers.ImageField(required=False)
    user = UserSerializer_email()

    class Meta:
        model = models.UserProfile
        fields = ['score', 'profileImage', 'user', "weight", "height", "city", "provinces", "sportPlaces", "weeklyGoal", "phoneNumber", "birth_date", "purposeSteps", "boostUser", "userProblem", "gender"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = data.pop('user')
        # Flatten the user data into the main dictionary
        data.update(user_data)
        return data

    def update(self, instance, validated_data):
        # Extract user data from the validated data
        user_data = validated_data.pop('user', None)
        sport_places = validated_data.pop('sportPlaces', None)
        boost_User = validated_data.pop('boostUser', None)

        # Update User model fields
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
            
        # Update UserProfile model fields
        if 'profileImage' in validated_data:
            instance.profileImage = validated_data['profileImage']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if sport_places is not None:
            instance.sportPlaces.set(sport_places)
        if boost_User is not None:
            instance.boostUser.set(boost_User)

        instance.save()
        return instance


# Update user information USER table in database
class UserUpdateFormSerializer(serializers.Serializer):
    userForm = UserSerializer()  # Use the UserSerializer
    userProfileForm = UserProfileSerializer()  # Use the UserProfileSerializer

    def update(self, instance, validated_data):
        # Extract the nested data
        userForm_data = validated_data.pop('userForm', None)
        userProfileForm_data = validated_data.pop('userProfileForm', None)

        # Update User instance
        if userForm_data:
            user_instance = instance[0]  # Assuming instance[0] is the User instance
            for attr, value in userForm_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        # Update UserProfile instance
        if userProfileForm_data:
            profile_instance = instance[1]  # Assuming instance[1] is the UserProfile instance
            for attr, value in userProfileForm_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()

        return instance
    