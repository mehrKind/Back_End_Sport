from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
# Create your models here.


class DailyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completeStep = models.PositiveIntegerField()
    traveledDistance = models.FloatField()
    calory = models.PositiveIntegerField()
    traveledTime = models.TimeField()
    dayDate = models.DateField(auto_now_add=True)
    dailyExercise = models.BooleanField(default = False)
    @property
    def totalStep(self):
        userprofile = UserProfile.objects.get(user = self.user)
        return userprofile.purposeSteps