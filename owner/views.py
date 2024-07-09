from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from owner import serializer
from owner import models
from account.models import UserProfile
from account.serializer import UserSerializer, UserProfileSerializer2
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime, time

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
        # Update the instance attributes by summing them with the values from request.data
        request.data["calory"] = instance.calory + request.data.get("calory", 0)
        request.data["completeStep"] = instance.completeStep + request.data.get("completeStep", 0)
        request.data["traveledDistance"] = instance.traveledDistance + request.data.get("traveledDistance", 0)
        # Get the last traveled time from the database
        last_traveled_time = instance.traveledTime

        # Convert the time object to datetime for addition with timedelta
        last_traveled_datetime = datetime.combine(datetime.min, last_traveled_time)

        # Calculate the new traveled time by adding minutes and seconds
        new_traveled_datetime = last_traveled_datetime + timedelta(minutes=request.data.get("travelMinutes", 0), seconds=request.data.get("travelSeconds", 0))

        # Extract the time component from the datetime object
        new_traveled_time = new_traveled_datetime.time()

        request.data["traveledTime"] = new_traveled_time
        
        if instance.totalStep <= instance.completeStep:
            print("yess")
        
        serializer_ = serializer.DailyInfoSerializer(instance, data=request.data, partial=True)
        if serializer_.is_valid():
            serializer_.save()
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "status": 400,
            "data": None,
            "error": serializer_.errors
        }
        return Response(context, status=status.HTTP_200_OK)

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
