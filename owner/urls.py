from django.urls import path, include
from owner import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path("daily_info/", views.UserDailyView.as_view()),
    path("history", views.HistoryView.as_view()),
    path("history/<int:pk>/delete/", views.HistoryView.as_view(), name='delete_history'),
    path("challenge", views.Challenge.as_view())
]