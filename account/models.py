from django.db import models
from django.contrib.auth.models import User


class SportPlace(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )

    user = models.OneToOneField(User, models.CASCADE)
    profileImage = models.ImageField(upload_to="media/UserProfile", default="default.jpg")
    phoneNumber = models.CharField(max_length=16)
    age = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=100)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    city = models.CharField(max_length=200, null=True, blank=True)
    provinces = models.CharField(max_length=200, null=True, blank=True)
    sportPlaces = models.ManyToManyField(SportPlace)
    purpesSteps = models.PositiveIntegerField(null=True)

    # def __str__(self):
    #     return f"{self.user.username} -> {self.provinces} - {self.city}"


class UserHealth(models.Model):
    HEALTH_STATUS = (
        ("بله ، مشکلی دارم", "بله ، مشکلی دارم"),
        ("نه ، ندارم", "نه ، ندارم"),
    )
    WEEKLY_GOALS = (
        ("1 بار در هفته", "1 بار در هفته"),
        ("2 بار در هفته", "2 بار در هفته"),
        ("3 بار در هفته", "3 بار در هفته"),
        ("بیش از 3 بار در هفته", "بیش از 3 بار در هفته"),
    )

    user = models.OneToOneField(User, models.CASCADE)
    healthProblem = models.CharField(choices=HEALTH_STATUS, max_length=100)
    healthProblemContent = models.TextField(blank=True, null=True)
    weeklyGoal = models.CharField(choices=WEEKLY_GOALS, max_length=100)

    def __str__(self):
        return f"{self.user.username} -> {self.healthProblem} - {self.weeklyGoal}"
