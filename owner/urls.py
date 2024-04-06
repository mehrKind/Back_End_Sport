from django.urls import path, include
from owner import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

daily_router = DefaultRouter()
daily_router.register(r"daily_info", views.UserDailyView, basename="daily_info")


urlpatterns = [
    path("", include(daily_router.urls)),
    path("history_user", views.HistoryView.as_view()),
]