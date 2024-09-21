from django.db import models
from django.contrib.auth.models import User
import string
import random

level_xp = [100, 200, 500, 1000, 2000, 10000, 50000, 100000, 500000, 1000000]
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# save the user sport place
class SportPlace(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BoostUser(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# generate the referrer code for the user
def generate_referrer_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

# save all information about the user (user profile)
class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )
    WEEKLY_GOALS = (
        ("1 بار در هفته", "1 بار در هفته"),
        ("2 بار در هفته", "2 بار در هفته"),
        ("3 بار در هفته", "3 بار در هفته"),
        ("بیش از 3 بار در هفته", "بیش از 3 بار در هفته"),
    )

    user = models.OneToOneField(User, models.CASCADE)
    profileImage = models.ImageField(upload_to="media/UserProfile", default="default.jpg")
    phoneNumber = models.CharField(max_length=16)
    birth_date = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=100)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    level = models.IntegerField(default=1)
    levelXp = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    city = models.CharField(max_length=200, null=True, blank=True)
    provinces = models.CharField(max_length=200, null=True, blank=True)
    sportPlaces = models.ManyToManyField(SportPlace)
    weeklyGoal = models.CharField(choices=WEEKLY_GOALS, max_length=100, null=True)
    purposeSteps = models.PositiveIntegerField(null=True, default=5000)
    boostUser = models.ManyToManyField(BoostUser)
    userProblem = models.TextField(null=True, blank=True)
    referrer_code = models.CharField(default=generate_referrer_code, max_length=7)
    related_referrer = models.ManyToManyField(User, related_name="related_profiles", blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is not in the database yet
            while UserProfile.objects.filter(referrer_code=self.referrer_code).exists():
                self.referrer_code = generate_referrer_code()

        # Calculate level based on score
        if self.score < 0:
            self.level = 1
        elif self.score < 100:
            self.level = 1
        elif self.score < 200:
            self.level = 2
        elif self.score < 500:
            self.level = 3
        elif self.score < 1000:
            self.level = 4
        elif self.score < 2000:
            self.level = 5
        elif self.score < 10000:
            self.level = 6
        elif self.score < 50000:
            self.level = 7
        elif self.score < 100000:
            self.level = 8
        elif self.score < 500000:
            self.level = 9
        else:
            self.level = 10  # For scores 500000 and above

        # Update levelXp based on the current level
        # Adjust the index as `level` is 1-based, so subtract 1 to get the correct index for `level_xp`
        if 1 <= self.level <= len(level_xp):
            self.levelXp = level_xp[self.level - 1]  # Adjusted to handle 0-indexing of the list

        # Now save the instance
        super().save(*args, **kwargs)
