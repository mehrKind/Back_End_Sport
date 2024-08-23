from django.urls import path, include
from owner import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

app_name = "owner"
urlpatterns = [
    path("daily_info/", views.UserDailyView.as_view(), name="daily_information"),
    path("daily_info/search/", views.UserDayInofo.as_view()),
    path("history/", views.HistoryView.as_view()),
    path("history/total/", views.TotalHistory.as_view()),
    path("history/<int:pk>/delete/", views.HistoryView.as_view(), name='delete_history'),
    path("challenge/", views.Challenge.as_view()),
    path("progress/", views.UserProgress.as_view(), name="userProgress")
]