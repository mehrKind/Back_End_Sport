from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from owner import serializer
from account import serializer as ac_serializer
from owner import models
from account.models import UserProfile
from account.serializer import UserSerializer, UserProfileSerializer2, UserProfileSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime, time
from django.db.models import Sum, Count, Max, Q
from django.db.models.functions import TruncWeek

# create a model for the daily user working: create and update

class UserDailyView(APIView):
    def get(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        # check if there is any daily work exist or not
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status" : 200,
                "data" : {
                    "is_firstTime" : False,
                    "values" : serializer_.data
                    },
                "error" : "null"
            }
            return Response(context, status.HTTP_200_OK)
        # if there was no item in the database for daily informaion
        else:
            context = {
                "status":404,
                "data" : {"is_firstTime" : True, "value" : []},
                "error": "no daily work were found :)"
            }
            return Response(context, status.HTTP_200_OK)
    # create daily work
    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer_ = serializer.DailyInfoSerializer(data=data)
        userprofile_queryset = UserProfile.objects.filter(user=request.user)
        profile_instance = get_object_or_404(userprofile_queryset)
        if userprofile_queryset.exists():
            new_score = profile_instance.score + request.data.get("score", 0) # sum the existing score with the new score came from request data
            profile_instance.score = new_score
            profile_instance.save()

        if serializer_.is_valid(): # serializer to save the new data with the post method
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
        #? update the overall score in the userProfile table
        userprofile_queryset = UserProfile.objects.filter(user=request.user)
        profile_instance = get_object_or_404(userprofile_queryset)
        # if anything was ok, save the update
        if userprofile_queryset.exists():
            new_score = profile_instance.score + request.data.get("score", 0) # sum the existing score with the new score came from request data
            profile_instance.score = new_score
            profile_instance.save()
        # if there was as item with the given date and user, update it. otherwise, call the post method
        if queryset.exists():
            # Update the instance attributes by summing them with the values from request.data
            request.data["calory"] = instance.calory + request.data.get("calory", 0)
            request.data["score"] = instance.score + request.data.get("score", 0)
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
            
            # if the user complete the daily steps change the bool object to True, else make it False
            if instance.totalStep <= instance.completeStep:
                request.data["dailyExercise"] = True
            
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
        else:
            return self.post(request, format=format)


# show the user daily information for specefic day
class UserDayInofo(APIView):
    def post(self, request, format=None):
        given_date = request.data.get("date")
        queryset = models.DailyInfo.objects.all().filter(dayDate = given_date)
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": 404,
                "data": "null",
                "error": f"there is no work for date: {given_date}"
            }
            return Response(context, status=status.HTTP_200_OK)
    def get(self, request, format=None):
        today_date = datetime.now().date()
        queryset = models.DailyInfo.objects.all().filter(dayDate = today_date)
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": 404,
                "data": "null",
                "error": "there is no work today"
            }
            return Response(context, status=status.HTTP_200_OK)  
        


# history workout

class HistoryView(APIView):
    # get method to have all user history, sum details and all daily work 
    def get(self, request, format=None):
        try:
            week_counter = request.GET.get("week")

            if week_counter is not None:
                week_counter = int(week_counter)  # Convert week_counter to an integer

                today = timezone.now().date()
                start_of_week = today - (week_counter * timedelta(days=today.weekday()))  # Start of the custom week
                end_of_week = start_of_week + timedelta(days=6 * week_counter)  # End of the counter week

                weekly_history = models.DailyInfo.objects.filter(
                    dayDate__range=[start_of_week, end_of_week]
                ).order_by('-dayDate')

                Historyserializer = serializer.DailyInfoSerializer(weekly_history, many=True)

                context = {
                    "status": 200,
                    "data": Historyserializer.data,
                    "error": None
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "status": 400,
                    "data": None,
                    "error": "Week parameter is missing or invalid"
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context = {
                "status": 500,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context = {
                "status": 500,
                "data": "null",
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)
        
    def delete(self, request, pk, format=None):
        try:
            activity = get_object_or_404(models.DailyInfo, pk=pk, user = request.user)
            activity.delete()
            context = {
                "status": 204,
                "data": f"activity with id : {pk} was deleted successfully",
                "error": "null" 
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                "status": 400,
                "data": "null",
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)
        
        
        
# history total items
# queryset = models.DailyInfo.objects.filter(user=request.user).order_by("-dayDate") # get and sort (date) data from daily table
# Historyserializer = serializer.DailyInfoSerializer(queryset, many=True) # make the last data as json (serialize)
# # sum columns
# totalSteps = queryset.aggregate(Sum('completeStep'))['completeStep__sum'] or 0
# totalDistance = queryset.aggregate(Sum('traveledDistance'))['traveledDistance__sum'] or 0
# totalCalory = queryset.aggregate(Sum('calory'))['calory__sum'] or 0

# total_time_seconds = sum([(td.traveledTime.hour * 3600 + td.traveledTime.minute * 60 + td.traveledTime.second) for td in queryset])

# total_time_minutes = total_time_seconds // 60
# total_time_seconds %= 60


class Challenge(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        leaderBoardType_request = request.GET.get("leaderBoardType")
        if leaderBoardType_request:
            leaderBoardType = leaderBoardType_request
        else:
            leaderBoardType = "weekly"

        if leaderBoardType == "weekly":
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Start of the current week
            end_of_week = start_of_week + timedelta(days=6)  # End of the current week

            # Calculate weekly scores
            weekly_scores = models.DailyInfo.objects.filter(
                dayDate__range=[start_of_week, end_of_week]
            ).values('user').annotate(total_score=Sum('score')).order_by('-total_score')

            # Get user profiles and merge with weekly scores
            user_profiles = UserProfile.objects.select_related('user')

            user_profile_dict = {profile.user.id: profile for profile in user_profiles}
            merged_data = []

            for counter, score_data in enumerate(weekly_scores, start=1):
                user_id = score_data['user']
                if user_id in user_profile_dict:
                    profile = user_profile_dict[user_id]
                    profile_serializer = UserProfileSerializer2(profile)
                    profile_data = profile_serializer.data
                    profile_data['score'] = score_data['total_score']
                    profile_data['rank'] = counter
                    merged_data.append(profile_data)

            context = {
                "status": 200,
                "data": {
                    "leaderBoardType": leaderBoardType,
                    "values": merged_data
                },
                "error": "null"
            }

            return Response(context, status=status.HTTP_200_OK)
        
        elif leaderBoardType == "overall":
            queryset = UserProfile.objects.select_related('user').all().order_by("-score")
            challengeSerializer = UserProfileSerializer2(queryset, many=True)

            # Adding rank to the serialized data
            merged_data = []
            for counter, data in enumerate(challengeSerializer.data, start=1):
                data["rank"] = counter
                merged_data.append(data)

            context = {
                "status": 200,
                "data": {
                    "leaderBoardType": leaderBoardType,
                    "values": merged_data
                },
                "error": "null"
            }

            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": 400,
                "data": "null",
                "error": f"bad request ! choose the correct leader board type. '{leaderBoardType}' is wrong"
            }

            return Response(context, status=status.HTTP_200_OK)