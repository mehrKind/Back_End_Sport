from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
# Create your models here.


class DailyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
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
    
    # if the user complete the daily steps change the bool object to True, else make it False
    def save(self, *args, **kwargs):
        if self.completeStep >= self.totalStep:
            self.dailyExercise = True
            return super(DailyInfo, self).save(*args, **kwargs)            
        else:
            self.dailyExercise = False
            return super(DailyInfo, self).save(*args, **kwargs)