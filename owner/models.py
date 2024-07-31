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
    dailyExercise = models.BooleanField(default=False)

    @property
    def totalStep(self):
        userprofile = UserProfile.objects.get(user=self.user)
        return userprofile.purposeSteps

    # if the user complete the daily steps change the bool object to True, else make it False
    def save(self, *args, **kwargs):
        if self.completeStep >= self.totalStep:
            self.dailyExercise = True
            return super(DailyInfo, self).save(*args, **kwargs)
        else:
            self.dailyExercise = False
            return super(DailyInfo, self).save(*args, **kwargs)


# ! add firend class
# ? https://www.youtube.com/watch?v=hyJO4mkdwuM

class FriendList(models.Model):
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return f"{self.user.username} | {self.user.email}"

    def add_friend(self, account):
        """_summary_

        Args:
            account (user): this is the user account who want to be add

        add new friends
        """

        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friends(self, account):
        """
        Args:
            account (user): this is the user who must be removed

        remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiade the action of unfriending someone
        """
        remover_friend_list = self
        # remove friend from remover friend list
        remover_friend_list.remove_friends(removee)
        
        # remove the friend from removee friend
        friend_list = FriendList.objects.get(user = removee)
        friend_list.remove_friends(self.user)
        
    def is_mutual_friend(self, friend):
        """
        is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False