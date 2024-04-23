from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from owner import serializer
from owner import models
from account.models import UserProfile
from account.serializer import UserProfileSerializer, UserSerializer
from rest_framework.decorators import APIView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404

# create a model for the daily user working: create and update

class UserDailyView(APIView):
    def get(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        serializer = serializer.DailyInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = serializer.DailyInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        filter_kwargs = {
            'user': request.user,
            'dayDate': request.data.get('dayDate', timezone.now().date())
        }
        instance = get_object_or_404(queryset, **filter_kwargs)
        serializer = serializer.DailyInfoSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# history 
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
        queryset = UserProfile.objects.all().order_by("-score")
        challengeSerializer = UserProfileSerializer(queryset, many=True)
        userQueryset = User.objects.values("username", "first_name")
        userChallengeSerializer = UserSerializer(userQueryset, many=True)
        data = challengeSerializer.data + userChallengeSerializer.data
        context = {
            "status":200,
            "data": data,
            "error":"null"
        }
        return Response(context, status.HTTP_200_OK)

