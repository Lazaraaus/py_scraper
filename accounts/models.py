# accounts/models.py 

# Imports 
from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser(AbstractUser):
    position = models.TextField(blank=True)
    is_searching = models.BooleanField(null=True) 
    skills = models.TextField(blank=True) 


# Create your models here.
