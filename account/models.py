from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )

    user = models.OneToOneField(User, models.CASCADE)
    profileImage = models.ImageField(upload_to="media/UserProfile", default="default.jpg")
    phoneNumber = models.CharField(max_length=16)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_TYPE, max_length=100)
    weight = models.IntegerField()
    height = models.IntegerField()
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    city = models.CharField(max_length=200, null=True, blank=True)
    provinces = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} -> {self.provinces} - {self.city}"
