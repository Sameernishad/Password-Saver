from django.db import models
from django.contrib.auth.models import User

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
