from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from owner import serializer
from owner import models
from account.models import UserProfile
from django.contrib.auth.models import User
from  rest_framework.decorators import APIView


# create a model for the daily user working: create and update
class UserDailyView(viewsets.ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = serializer.DailyInfoSerializer

    def get_queryset(self):
        # replace models.DailyInfo with your actual model
        # add your logic here
        return models.DailyInfo.objects.filter(user = self.request.user)

    # add daily work
    def create(self, request):
        DailySerializer = self.get_serializer(data = request.data)
        if DailySerializer.is_valid():
            DailySerializer.save()
            context = {
                "status": 200,
                "data":f"{DailySerializer.data}",
                "error":"null"
            }
            return Response(context, status.HTTP_200_OK)
        else:
            context = {
                "status": 400,
                "data":"null",
                "error": f"{DailySerializer.errors}"
            }
            return Response(context, status.HTTP_200_OK)


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