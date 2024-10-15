from django.urls import path
from step import views


app_name = "step"
urlpatterns = [
    # path("support/", views.SupportView.as_view(), name="support"),
    path("settings", views.SettingsView.as_view(), name="settings")
]
