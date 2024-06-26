from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router1 = DefaultRouter()
router1.register(r"contact-us", views.ContactUsView, basename="ContactUsView")


urlpatterns = [
    path("", views.main_api),
    path('', include(router1.urls))
]
