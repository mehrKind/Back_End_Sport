from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from owner import serializer
from owner import models
from account.models import UserProfile
from account.serializer import UserSerializer, UserProfileSerializer2
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.db.models import Sum, F

# create a model for the daily user working: create and update


class UserDailyView(APIView):
    def get(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        # check if there is any daily work exist or not
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": {
                    "is_firstTime": False,
                    "values": serializer_.data
                },
                "error": "null"
            }
            return Response(context, status.HTTP_200_OK)
        # if there was no item in the database for daily informaion
        else:
            context = {
                "status": 404,
                "data": {"is_firstTime": True, "value": []},
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
            # sum the existing score with the new score came from request data
            new_score = profile_instance.score + request.data.get("score", 0)
            profile_instance.score = new_score
            profile_instance.save()

        if serializer_.is_valid():  # serializer to save the new data with the post method
            serializer_.save()
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "status": 400,
            "data": "null",
            "error": serializer_.errors
        }
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        queryset = models.DailyInfo.objects.filter(user=request.user)
        filter_kwargs = {
            'user': request.user,
            'dayDate': request.data.get('dayDate', timezone.now().date())
        }

        # if there was nothing to update, call the post func and post the request data
        try:
            instance = get_object_or_404(queryset, **filter_kwargs)
        except:
            return self.post(request, format=format)

        # ? update the overall score in the userProfile table
        userprofile_queryset = UserProfile.objects.filter(user=request.user)
        profile_instance = get_object_or_404(userprofile_queryset)
        # if anything was ok, save the update
        if userprofile_queryset.exists():
            # sum the existing score with the new score came from request data
            new_score = profile_instance.score + request.data.get("score", 0)
            profile_instance.score = new_score
            profile_instance.save()
        # if there was as item with the given date and user, update it. otherwise, call the post method
        if queryset.exists():
            # Update the instance attributes by summing them with the values from request.data
            request.data["calory"] = instance.calory + \
                request.data.get("calory", 0)
            request.data["score"] = instance.score + \
                request.data.get("score", 0)
            request.data["completeStep"] = instance.completeStep + \
                request.data.get("completeStep", 0)
            request.data["traveledDistance"] = instance.traveledDistance + \
                request.data.get("traveledDistance", 0)
            # Get the last traveled time from the database
            last_traveled_time = instance.traveledTime

            # Convert the time object to datetime for addition with timedelta
            last_traveled_datetime = datetime.combine(
                datetime.min, last_traveled_time)

            # Calculate the new traveled time by adding minutes and seconds
            new_traveled_datetime = last_traveled_datetime + \
                timedelta(minutes=request.data.get("travelMinutes", 0),
                          seconds=request.data.get("travelSeconds", 0))

            # Extract the time component from the datetime object
            new_traveled_time = new_traveled_datetime.time()

            request.data["traveledTime"] = new_traveled_time

            # if the user complete the daily steps change the bool object to True, else make it False
            # if instance.totalStep <= instance.completeStep:
            #     request.data["dailyExercise"] = True

            serializer_ = serializer.DailyInfoSerializer(
                instance, data=request.data, partial=True)
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


class UserProgress(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()

        # Adjusting to consider Saturday as the first day of the week and Friday as the last
        # Start of the current week (Saturday)
        start_of_week = today - timedelta(days=(today.weekday() + 2) % 7)
        # End of the current week (Friday)
        end_of_week = start_of_week + timedelta(days=6)

        # This week dates
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

        # Initialize percent_list with default values
        percent_list = [{"percent": 0, "day": int(
            day.strftime("%d"))} for day in week_dates]

        # Filter the progress date
        user_progress = models.DailyInfo.objects.filter(
            user=request.user,
            dayDate__range=(start_of_week, end_of_week)
        )

        # Serialize data
        user_progress_serializer = serializer.DailyInfoSummarySerializer(
            user_progress, many=True)

        # Create a dictionary for quick lookup
        progress_dict = {
            entry["dayDate"]: entry for entry in user_progress_serializer.data}

        # Iterate through the week_dates and update percent_list if data exists
        for i, day in enumerate(week_dates):
            day_str = day.strftime("%Y-%m-%d")

            if day_str in progress_dict:
                try:
                    complete_step = int(
                        progress_dict[day_str].get("completeStep", 0))
                    total_step = int(
                        progress_dict[day_str].get("totalStep", 0))

                    # Avoid division by zero
                    if total_step > 0:
                        percent = (complete_step / total_step) * 100
                        # Cap the percentage at 100%
                        percent = min(percent, 100)
                        # Update the percent for the specific day
                        percent_list[i]["percent"] = int(percent)
                except (ValueError, KeyError):
                    pass  # Keep the default percent value of 0

        # Return the data
        context = {
            "status": 200,
            "data": percent_list,
            "error": "null"
        }

        return Response(context, status=status.HTTP_200_OK)

# show the user daily information for specefic day


class UserDayInofo(APIView):
    def post(self, request, format=None):
        given_date = request.data.get("date")
        queryset = models.DailyInfo.objects.all().filter(dayDate=given_date)
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": serializer_.data[0],
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
        queryset = models.DailyInfo.objects.all().filter(
            dayDate=today_date).filter(user=request.user)
        if queryset:
            serializer_ = serializer.DailyInfoSerializer(queryset, many=True)
            context = {
                "status": 200,
                "data": serializer_.data[0],
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
                # Convert week_counter to an integer
                week_counter = int(week_counter)

                today = timezone.now().date()
                print(f"today: {today}")
                # Start of the custom week
                start_of_week = today - \
                    timedelta(days=today.weekday() + 7 * week_counter)
                print(f"start_of_week: {start_of_week}")
                end_of_week = start_of_week + \
                    timedelta(days=6)  # End of the counter week
                print(f"end_of_week: {end_of_week}")

                weekly_history = models.DailyInfo.objects.filter(
                    dayDate__range=[start_of_week, end_of_week],
                    user=request.user
                ).order_by('-dayDate')

                history_serializer = serializer.DailyInfoSerializer(
                    weekly_history, many=True)

                context = {
                    "status": 200,
                    "data": history_serializer.data,
                    "error": "null"
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "status": 400,
                    "data": "null",
                    "error": "Week parameter is missing or invalid"
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
            activity = get_object_or_404(
                models.DailyInfo, pk=pk, user=request.user)
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


# invited users

class InvitedUser(APIView):
    # Get all users who I invited to the app
    def get(self, request):
        try:
            userProfile = models.UserProfile.objects.get(user=request.user)
            # Get all users invited by the current user
            invited_users = userProfile.related_referrer.all()

            # Prepare a list to hold invited users' data
            invited_users_data = []

            for invited_user in invited_users:
                invited_profile_user = models.UserProfile.objects.get(
                    user=invited_user)
                invited_users_data.append({
                    "userId": invited_profile_user.user.id,
                    "username": invited_profile_user.user.username,
                    # "fullname": invited_profile_user.user.first_name,
                    "profileImage": invited_profile_user.profileImage.url if invited_profile_user.profileImage else None,
                    "level": invited_profile_user.level,
                    "score": invited_profile_user.score
                })

            context = {
                "status": 200,
                "data": invited_users_data,
                "error": "null"
            }

            return Response(context, status=status.HTTP_200_OK)

        except models.UserProfile.DoesNotExist:
            context = {
                "status": 404,
                "data": "null",
                "error": "User profile does not exist."
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                "status": 500,
                "data": "null",
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)


# history total items

class TotalHistory(APIView):
    def get(self, request, foramt=None):
        totalQuerySet = models.DailyInfo.objects.all().filter(
            user=request.user)  # get and sort (date) data from daily table
        # sum columns
        totalSteps = totalQuerySet.aggregate(Sum('completeStep'))[
            'completeStep__sum'] or 0
        totalDistance = totalQuerySet.aggregate(Sum('traveledDistance'))[
            'traveledDistance__sum'] or 0
        totalCalory = totalQuerySet.aggregate(
            Sum('calory'))['calory__sum'] or 0

        total_time_seconds = sum([(td.traveledTime.hour * 3600 + td.traveledTime.minute *
                                 60 + td.traveledTime.second) for td in totalQuerySet])

        total_time_minutes = total_time_seconds // 60
        total_time_seconds %= 60

        context = {
            "status": 200,
            "data": {
                "totalSteps": totalSteps,
                "totalDistance": totalDistance,
                "totalCalory": totalCalory,
                "travedTime": f"{total_time_minutes}:{total_time_seconds}",

            },
            "error": "null"
        }
        return Response(context, status=status.HTTP_200_OK)


class Challenge(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        leaderBoardType_request = request.GET.get("leaderBoardType")
        leaderBoardType = leaderBoardType_request if leaderBoardType_request else "weekly"
        # weekly users informations
        if leaderBoardType == "weekly":
            try:
                today = timezone.now().date()
                # Start of the current week
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + \
                    timedelta(days=6)  # End of the current week

                # Calculate weekly scores and other metrics
                weekly_aggregates = models.DailyInfo.objects.filter(
                    dayDate__range=[start_of_week, end_of_week]
                ).values('user').annotate(
                    total_score=Sum('score'),
                    total_complete_step=Sum('completeStep'),
                    total_traveled_distance=Sum('traveledDistance'),
                    total_calory=Sum('calory'),
                    total_traveled_time=Sum(F('traveledTime__hour') * 3600 + F('traveledTime__minute') * 60 + F(
                        'traveledTime__second'))  # Sum of traveled time in seconds
                ).order_by('-total_score')

                # Get user profiles and merge with weekly aggregates
                user_profiles = UserProfile.objects.select_related('user')

                user_profile_dict = {
                    profile.user.id: profile for profile in user_profiles}
                merged_data = []
                mySelfInfinormation = {}

                for counter, aggregate_data in enumerate(weekly_aggregates, start=1):
                    user_id = aggregate_data['user']
                    if user_id in user_profile_dict:
                        profile = user_profile_dict[user_id]
                        profile_serializer = UserProfileSerializer2(profile)
                        profile_data = profile_serializer.data

                        # Add the weekly aggregates to the profile data
                        profile_data['score'] = aggregate_data['total_score']
                        profile_data['completeStep'] = aggregate_data['total_complete_step']
                        profile_data['traveledDistance'] = aggregate_data['total_traveled_distance']
                        profile_data['calory'] = aggregate_data['total_calory']
                        profile_data['traveledTime'] = aggregate_data['total_traveled_time']
                        profile_data['rank'] = counter

                        merged_data.append(profile_data)
                # find the user that is online now and get his rank
                for item in merged_data:
                    if item["username"] == request.user.username:
                        mySelfInfinormation = item
                        break

                context = {
                    "status": 200,
                    "data": {
                        "leaderBoardType": "weekly",
                        "mySelfInformation": mySelfInfinormation,
                        "values": merged_data
                    },
                    "error": "null"
                }

                return Response(context, status=status.HTTP_200_OK)
            except Exception as e:
                context = {
                    "status": 500,
                    "data": "null",
                    "error": str(e)
                }
                return Response(context, status=status.HTTP_200_OK)
        # overall inforamtion challenge
        elif leaderBoardType == "overall":
            try:
                # Calculate overall scores and other metrics
                overall_aggregates = models.DailyInfo.objects.values('user').annotate(
                    total_score=Sum('score'),
                    total_complete_step=Sum('completeStep'),
                    total_traveled_distance=Sum('traveledDistance'),
                    total_calory=Sum('calory'),
                    total_traveled_time=Sum(F('traveledTime__hour') * 3600 + F('traveledTime__minute') * 60 + F(
                        'traveledTime__second'))  # Sum of traveled time in seconds
                ).order_by('-total_score')

                # Get user profiles and merge with overall aggregates
                user_profiles = UserProfile.objects.select_related('user')

                user_profile_dict = {
                    profile.user.id: profile for profile in user_profiles}
                merged_data = []
                mySelfInfinormation = {}
                for counter, aggregate_data in enumerate(overall_aggregates, start=1):
                    user_id = aggregate_data['user']
                    if user_id in user_profile_dict:
                        profile = user_profile_dict[user_id]
                        profile_serializer = UserProfileSerializer2(profile)
                        profile_data = profile_serializer.data

                        # Add the overall aggregates to the profile data
                        profile_data['score'] = aggregate_data['total_score']
                        profile_data['completeStep'] = aggregate_data['total_complete_step']
                        profile_data['traveledDistance'] = aggregate_data['total_traveled_distance']
                        profile_data['calory'] = aggregate_data['total_calory']
                        profile_data['traveledTime'] = aggregate_data['total_traveled_time']
                        profile_data['rank'] = counter

                        merged_data.append(profile_data)

                # find the user that is online now and get his rank
                for item in merged_data:
                    if item["username"] == request.user.username:
                        mySelfInfinormation = item
                        break

                context = {
                    "status": 200,
                    "data": {
                        "leaderBoardType": "overall",
                        "mySelfInformation": mySelfInfinormation,
                        "values": merged_data[:10]
                    },
                    "error": "null"
                }

                return Response(context, status=status.HTTP_200_OK)
            except Exception as e:
                context = {
                    "status": 500,
                    "data": "null",
                    "error": str(e)
                }
                return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": 400,
                "data": "null",
                "error": f"Bad request! Choose the correct leaderboard type. '{leaderBoardType}' is incorrect."
            }

            return Response(context, status=status.HTTP_200_OK)
