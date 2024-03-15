from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework import viewsets
from .sertializer import ContactSerializer
from .models import ContactUs_db
from django.core.mail import send_mail
from django.conf import settings
from random import randint


def main_api(request):
    if request.method == "GET":
        global random_number
        reception_list = ["pmehraban17@gmail.com"]
        random_number = randint(1000, 9999)
        try:
            send_mail("باز یابی رمز عبور", f"کد چهار رقمی {random_number} را وارد کنید ",
                      settings.EMAIL_HOST, reception_list, fail_silently=False)
            print("========================================")
            print("message sent")
            print(f"random number => {random_number}")
            print("========================================")
        except:
            print("message did not sent")

    if request.method == "POST":
        digit_number = request.POST.get("digit")
        if int(digit_number) == random_number:
            print(True)
            print(random_number)
            print(digit_number)
        else:
            print(False)
            print(random_number)
            print(digit_number)

    return render(request, "test.html")



class ContactUsView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    # get the current user that has been logged in to the site
    def get_queryset(self):
        user = self.request.user
        queryset = ContactUs_db.objects.filter(user=user).all()
        return queryset

