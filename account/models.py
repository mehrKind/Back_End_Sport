from django.db import models
from django.contrib.auth.models import User
import string
import random

class SportPlace(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# generate the referrer code for the user
import string
import random
from django.db import models
from django.contrib.auth.models import User

def generate_referrer_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )

    user = models.OneToOneField(User, models.CASCADE)
    profileImage = models.ImageField(upload_to="media/UserProfile", default="default.jpg")
    phoneNumber = models.CharField(max_length=16)
    # age = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=100)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    city = models.CharField(max_length=200, null=True, blank=True)
    provinces = models.CharField(max_length=200, null=True, blank=True)
    sportPlaces = models.ManyToManyField(SportPlace)
    purpesSteps = models.PositiveIntegerField(null=True)
    referrer_code = models.CharField(default=generate_referrer_code, max_length=7)

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is not in the database yet
            while UserProfile.objects.filter(referrer_code=self.referrer_code).exists():
                self.referrer_code = generate_referrer_code()
        super().save(*args, **kwargs)


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
