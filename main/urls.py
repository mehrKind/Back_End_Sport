from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router1 = DefaultRouter()
router1.register("", views.ContactUsView, basename="ContactUsView")


urlpatterns = [
    path('', include(router1.urls), name="contactusView"),
]
