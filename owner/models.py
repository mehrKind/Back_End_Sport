from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DailyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completeStep = models.PositiveIntegerField()
    traveledDistance = models.FloatField()
    kalory = models.PositiveIntegerField()
    traveledTime = models.TimeField()
    dayDate = models.DateField()
    dailyExercise = models.BooleanField(default = False)