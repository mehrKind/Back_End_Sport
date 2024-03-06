from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework import viewsets
from .sertializer import ContactSerializer
from .models import ContactUs_db

def main_api(request):
    return HttpResponse("<h1><a href='/admin'>Admin Panel</a></h1>")


class ContactUsView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    # get the current user that has been logged in to the site
    def get_queryset(self):
        user = self.request.user
        queryset = ContactUs_db.objects.filter(user=user).all()
        return queryset

