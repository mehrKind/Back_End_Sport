from django.db import models
from django.contrib.auth.models import User


class ContactUs_db(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    textBody = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.textBody[:10]}..."
