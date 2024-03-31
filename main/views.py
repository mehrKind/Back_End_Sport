from django.shortcuts import render
from rest_framework import viewsets
from .sertializer import ContactSerializer
from .models import ContactUs_db
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


def main_api(request):
    return render(request, "test.html")



class ContactUsView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    # permission_classes = [AllowAny]

    # get the current user that has been logged in to the site
    def get_queryset(self):
        user = self.request.user
        queryset = ContactUs_db.objects.filter(user=user).all().order_by("-send_date")
        return queryset

    def create(self, request):
        user = request.user
        textBody = request.data.get("textBody")

        # check  if the textarea is not empty
        if textBody is None:
            return Response({"detail":"no text body provided"}, status.HTTP_400_BAD_REQUEST)
        
        # insert to the database
        ContactUs_db.objects.create(user = user, textBody = textBody)
        return Response({"detail":"succuess send message"}, status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def message_count(self, request):
        user = request.user
        count = ContactUs_db.objects.filter(user=user).count()
        return Response({"count": count})