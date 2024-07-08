from django.urls import path, include
from owner import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path("daily_info/", views.UserDailyView.as_view()),
    path("history_user", views.HistoryView.as_view()),
    path("challenge", views.Challenge.as_view())
]