from django.db import models
from django.contrib.auth.models import User


class StepSupport(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_message = models.TextField()
    receiver_message = models.TextField(null=True, blank=True)
    sender_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the message is created
    receiver_date = models.DateTimeField(auto_now_add=True)  # Optional field for when the receiver responds

    def __str__(self):
        return f"Message from {self.sender} on {self.sender_date}"
