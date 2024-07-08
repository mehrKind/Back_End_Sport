from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from owner import serializer
from owner import models
from account.models import UserProfile
from account.serializer import UserProfileSerializer, UserSerializer, UserProfileSerializer2
from rest_framework.decorators import APIView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404

# create a model for the daily user working: create and update

class UserDailyView(APIView):
    def get(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        # check if there is any daily work exist or not
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status" : 200,
                "data" : serializer_.data,
                "error" : "null"
            }
            return Response(context, status.HTTP_200_OK)
        # if there was no item in the database for daily informaion
        else:
            context = {
                "status":404,
                "data" : "null",
                "error": "no daily work were found :)"
            }
            return Response(context, status.HTTP_200_OK)
    # create daily work
    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer_ = serializer.DailyInfoSerializer(data=data)
        if serializer_.is_valid():
            serializer_.save()
            context = {
                "status" : 200,
                "data" : serializer_.data,
                "error" : "null"
            }
            return Response(context ,status=status.HTTP_200_OK)
        context = {
            "status" : 400,
            "data": "null",
            "error" : serializer_.errors
        }
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        filter_kwargs = {
            'user': request.user,
            'dayDate': request.data.get('dayDate', timezone.now().date())
        }
        instance = get_object_or_404(queryset, **filter_kwargs)
        serializer_ = serializer.DailyInfoSerializer(instance, data=request.data, partial=True)
        if serializer_.is_valid():
            serializer_.save()
            context = {
                "status" : 200,
                "data" : serializer_.data,
                "error" : "null"
            }
            return Response(context, status.HTTP_200_OK)
        context = {
            "status" : 400,
            "data": "null",
            "error" : serializer_.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

# history workout
class HistoryView(APIView):
    def get(self, request, format=None):
        try:
            queryset = models.DailyInfo.objects.all().order_by("-dayDate").filter(user = request.user)  # Fetch the data from your model
            Historyserializer = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": Historyserializer.data,
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            # Create a context with the error message
            context = {
                "status": 500,
                "data": "null",
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)
        


class Challenge(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # queryset = UserProfile.objects.all().order_by("-score")
        queryset = UserProfile.objects.all().order_by("-score")
        challengeSerializer = UserProfileSerializer2(queryset, many=True)
        userQueryset = User.objects.values("username", "first_name", "last_login")
        userChallengeSerializer = UserSerializer(userQueryset, many=True)
        # merge two dics togather
        merged_data = []
        for profile, user in zip(challengeSerializer.data, userChallengeSerializer.data):
            merged_item = profile.copy()
            merged_item.update(user)
            merged_data.append(merged_item)

        context = {
            "status": 200,
            "data": merged_data,
            "error": "null"
        }

        return Response(context, status=status.HTTP_200_OK)
