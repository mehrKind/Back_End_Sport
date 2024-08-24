from django.shortcuts import render
from rest_framework import viewsets
from .sertializer import ContactSerializer
from .models import ContactUs_db
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


def main_api(request):
    return render(request, "home.html")