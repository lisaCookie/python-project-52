# users/models.py

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # добавьте дополнительные поля при необходимости

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name