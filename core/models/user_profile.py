"""
Created on 24 de jul. de 2025

@author: masterdev
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ddd = models.CharField(max_length=3)
    mobile_number = models.CharField(max_length=15)
    # outros campos úteis: nome completo, CPF, etc.
